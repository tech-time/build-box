from jenkinsapi.jenkins import Jenkins
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class BuildBoxJenkins:
    def __init__(self, jenkins_url, username, password):
        self._jenkins = Jenkins(jenkins_url, username=username, password=password, ssl_verify=False)
        self._views = self._jenkins.views

    def get_jobs_from_view(self, view_name) -> object:
        view = self._views[view_name]
        if view == None:
            return []
        return [job_name for job_name, job in view.items()]

    def get_builds_from_job(self, job_name):
        job = self._jenkins.get_job(job_name)
        hist_val = []
        laststatus = "NO BUILD"
        lastid = -1
        for build_id in job.get_build_ids():
            status = job.get_build(build_id).get_status()
            if build_id > lastid and status != None:
                laststatus = status
                lastid = build_id
            hist_val.append(status)
        return (hist_val, laststatus)

