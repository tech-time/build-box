from jenkinsapi.jenkins import Jenkins
from jenkinsapi.views import Views

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class BuildBoxJenkins:
    def __init__(self, jenkins_url, username, password):
        self._jenkins = Jenkins(jenkins_url, username=username, password=password, ssl_verify=False)
        self._views = self._jenkins.views
        self._jobs = {}


    def get_view_info(self, view_name: object) -> object:
        view = self._views[view_name]
        ret_val = {}
        self._jobs = {}
        for job_name, job in view.items():
            self._jobs[job_name] = job
            ret_val[job_name] = job.get_last_build().is_good()
        return ret_val

    def get_previous_build_results(self, job_name):
        job = self._jobs[job_name]
        ret_val = {}
        for build_id in job.get_build_ids():
            ret_val[build_id] = job.get_build(build_id).get_status()
        return ret_val
