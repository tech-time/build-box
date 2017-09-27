import pytest
import os

from buildbox.ci import BuildBoxJenkins

def test_jenkins():
    jenkins_url = "https://factory-ixxi.noisy.ratp/jenkins"
    view = "API_IXXI_1545"
    f = open(os.path.expanduser('~') + "/.mdp", "r")
    username,password=f.read().rstrip().split(":")
    jenkins = BuildBoxJenkins(jenkins_url, username, password)
    info = jenkins.get_view_info(view)