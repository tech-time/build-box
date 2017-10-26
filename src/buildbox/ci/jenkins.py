import jenkinsapi
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.views import Views
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class BuildBoxJenkins:
    def __init__(self, jenkins_url, username, password):
        self._jenkins = Jenkins(jenkins_url, username = username, password = password, ssl_verify = False)
        self._views = Views(self._jenkins)
    
    def get_view_info(self, view_name):
        view = self._views[view_name]
        ret_val = {}
        for job_name, job in view.items():
            ret_val[job_name] = job.get_last_build().is_good()
        return ret_val

