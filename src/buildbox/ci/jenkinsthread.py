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


    def __init__(self, jenkins_url, jenkins_views):
        f = open(os.path.expanduser('~') + "/.mdp", "r")
        username, password = f.read().rstrip().split(":")
        self._bbj = BuildBoxJenkins(jenkins_url, username, password)

        self._views = jenkins_views
        self._builds = {}
        self._buildIndex = 0
        self._viewIndex = 0
        self.time_interval = 5
        self.get_builds()
        self.speed = 5
        super().__init__(daemon=True)
        self.name = 'Jenkins Thread'
        self.start()

    def get_builds(self):
        view = self._views[self._viewIndex]
        print("--------------------- get_builds from " + view)
        info = self._bbj.get_view_info(view)

        builds = []
        for job_name in info:
            last = info[job_name]
            history = self._bbj.get_previous_build_results(job_name)
            builds.append(BuildItem(last, history, job_name))
        self._builds[view] = builds
        self._viewIndex += 1
        if self._viewIndex == len(self._views):
            self._viewIndex = 0
        print("--------------------- get_builds END")

    def getNextBuild(self):
        view = self._views[self._viewIndex]
        builds = self._builds[view]
        last_build = builds[self._buildIndex]
        self._buildIndex += 1
        if self._buildIndex == len(builds):
            self._buildIndex = 0
            self._viewIndex += 1
            if self._viewIndex == len(self._views):
                self._viewIndex = 0
        return last_build

    def run(self):
        while True:
            print("Waiting : %d" % self.speed)
            time.sleep(self.speed)
            self.get_builds()


class BuildItem():
    health_period = -1

    def __init__(self, l, hist, n):
        self.last = l
        if BuildItem.health_period == -1:
            self.history = hist
        else:
            self.history={}
            for h in hist:
                self.history[h] = hist[h]
                if (len(self.history) == BuildItem.health_period):
                    break
        self.name = n
        self.health = -1  # % of failed builds in all last results, -1 if unknown
        if len(hist) > 0:
            self.health = 100 * len([h for h in hist if (hist[h] == "SUCCESS")]) / len(hist)
