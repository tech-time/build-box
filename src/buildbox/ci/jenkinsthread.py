'''
Build interface
 - initialise interface with Build server (Jenkins)
 - interface with build server to get build results


 Build results contain:
  - A status indicator (from 0 to 100)
  - A health indicator (sunny or cloudy)
  - a project name


  TODO : import jenkinsapi, connect to the server, read a list of builds from config file and translate job results
'''
import time
import os
from threading import Thread

from src.buildbox.ci import BuildBoxJenkins


class JenkinsThread(Thread):
    speed = 1

    def __init__(self, jenkins_url, view_Names, job_Names):
        f = open(os.path.expanduser('~') + "/.mdp", "r")
        username, password = f.read().rstrip().split(":")
        self._bbj = BuildBoxJenkins(jenkins_url, username, password)
        self._views = view_Names
        self._jobs = job_Names
        # Adding a new "empty" view to hold all the individual jobs
        if (len(job_Names) != 0):
            self._views = [""] +  view_Names
        self._job_dict = {}         # Job list retrieved from the Jenkisn server, indexed by job name
        self._job_list = []
        self._jobIndex = -1
        self.time_interval = 5

        super().__init__(daemon=True)
        self.name = 'Jenkins Thread'
        self.start()

    # Skip some jobs (usually 1 to get to the next one)
    def skipJobs(self, amount):
        if len(self._job_list)>0:
            self._jobIndex += amount
            if self._jobIndex >= len(self._job_list):
                self._jobIndex = 0


    # Fetch an item to display : method used by other threads to get some job data (when available)
    def getNextBuild(self):
        if len(self._job_list)>0:
            self.skipJobs(1)
            return self._job_list[self._jobIndex]

    def run(self):
        while True:
            for view in self._views:
                if view == "":
                    jn_list = self._jobs
                else:
                    jn_list = self._bbj.get_jobs_from_view(view)
                for job_name in jn_list:
                     hist, status = self._bbj.get_builds_from_job(job_name)
                     if job_name in self._job_dict:
                         jj = self._job_dict[job_name]
                         jj.set(hist, status, view)
                     else:
                         jj = JenkinsJob(job_name, hist, status, view )
                         self._job_dict[job_name] = jj
                         self._job_list.append(jj)
                     time.sleep(JenkinsThread.speed)



class JenkinsJob():
    health_period = -1

    def __init__(self, n, hist, l, v):
        self.view = v
        self.last = l
        self.name = n  # build name
        self.health = -1
        self.set_history(hist)

    def set(self, hist, l, v):
        self.view = v
        self.last = l
        self.set_history(hist)    # % of failed builds in all last results, -1 if unknown

    def set_history(self, hist):
        self.health = -1
        self.history = hist
        if JenkinsJob.health_period == -1:
            healthlist = hist
        else:
            healthlist = hist[:JenkinsJob.health_period]
        if len(hist) > 0:
            self.health = 100 * len([h for h in healthlist if (h == "SUCCESS")]) / len(healthlist)
