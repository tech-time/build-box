import pytest
import os

from buildbox.ci import BuildBoxJenkins

# TODO: find an infrastructure agnostic way to test api or make the test optional
def test_jenkins():
    jenkins_url = "https://factory-ixxi.noisy.ratp/jenkins"
    view = "API_IXXI_1545"
    filename = os.path.join(os.path.expanduser('~'), ".mdp")
    f = open(filename, "r")
    username,password=f.read().rstrip().split(":")
    jenkins = BuildBoxJenkins(jenkins_url, username, password)
    info = jenkins.get_jobs_from_view(view)
