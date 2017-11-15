import os
import time
import colorsys

from .ci.jenkinsthread import JenkinsThread, JenkinsJob
import jenkinsapi.custom_exceptions
from .devices import DigitalDisplay, GraphicDisplay, RGBLeds
from .conf import BuildboxParameter

from PIL import Image


# Utility function (not used)
def get_all_views(vl):
    # get all views from jenkins server in a format that can be used in buildbox ini file
    for (k, v), i in zip(vl.iteritems(), range(1,len(vl)+1)):
        print("view%d: %s" % (i, k))
def get_all_jobs(jl):
    # get all jobs from jenkins server in a format that can be used in buildbox ini file
    for (k, v), i in zip(jl.iteritems(), range(1, len(jl)+1)):
        print("job%d: %s" % (i, k))

def main():
    print("Hello World!")

    STATUS_COLOR = {"SUCCESS":   RGBLeds.COLOR_GREEN,   # GREEN
                    "UNSTABLE":  RGBLeds.COLOR_RED,     # YELLOW
                    "FAILURE":   RGBLeds.COLOR_YELLOW,  # RED
                    "NOT_BUILT": RGBLeds.COLOR_GREY,    # GREY
                    "ABORTED":   RGBLeds.COLOR_GREY,    # GREY
                    "NO BUILD":  RGBLeds.COLOR_GREY     # GREY
                    }
    STATUS_MSG = {  "SUCCESS":   "PASS",
                    "UNSTABLE":  "FAIL",
                    "FAILURE":   "FAIL",
                    "NOT_BUILT": "____",
                    "ABORTED":   "FAIL",
                    "NO BUILD":  "____"}

    # iconfile = "../../health-icons 32x32.bmp"
    iconfile = "buildbox/ressources/health-icons NB 32x32.bmp"
    healthiconlist = (Image.open(iconfile).crop((  0, 0,  32, 32)),  # No recent builds failed -> health > 80%
                      Image.open(iconfile).crop(( 33, 0,  64, 32)),  # 20-40% of recent builds failed
                      Image.open(iconfile).crop(( 65, 0,  96, 32)),  # 40-60% of recent builds failed
                      Image.open(iconfile).crop(( 97, 0, 128, 32)),  # 60-80% of recent builds failed
                      Image.open(iconfile).crop((129, 0, 160, 32)))  # all recent builds failed (> 80%)

    dd = DigitalDisplay()
    gd = GraphicDisplay()
    ld = RGBLeds()

    def error(test, msg, abort=False, rgbledscolor = RGBLeds.COLOR_RED, ddmsg = "Err", delay=5):
        if test:
            dd.display(ddmsg)
            ld.display_all(rgbledscolor)
            gd.clear()
            gd.displaytext(2, 2, msg[:21])
            gd.displaytext(2, 14, msg[21:])
            time.sleep(delay)
            if abort:
                exit(-1)

    # ------------------------------------------------------------------------------------
    # Start of old stuff : to remove later
    step = 0
    for i in range(5):
        gd.clear()
        if step == 0:
            gd.displaytext(2, 2, "/--- Dude Cool !---\\")
            dd.display('dudE')
        else:
            gd.displaytext(2, 2, "/--- Cool Dude !---\\")
            dd.display('COOL')
        step = (step + 1) % 2
        gd.displaytext(2, 14, "\____<________>____/")
        gd.displaytext(2, 26, 'Status=PASS')
        gd.displayicon(72, 26, healthiconlist[int((100 - i * 5) / 20) - 1])

        hue = int(time.time() * 100) % 360
        color_list = []
        for x in range(8):
            offset = x * 360.0 / 16.0
            h = ((hue + offset) % 360) / 360.0
            color_list.append([int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)])
        ld.display(color_list)
        time.sleep(0.1)
    # END of old stuf : to remove later
    # ------------------------------------------------------------------------------------

    # Display waiting message
    error(True, 'BuildBox start       Fetching jobs ...', False, RGBLeds.COLOR_GREY,"____", 0)

    # Get parameters from parameter file
    params = BuildboxParameter(os.path.expanduser('~') + "/.buildbox")
    params.readConfigurationFromIniFile()

    # Jenkins server URL
    jenkins_url = params.getParam("url")                        # = "https://xxxxxxx/jenkins"
    error(jenkins_url == "", "Jenkins URL error", abort=True)

    # Views to display
    jenkins_views = [view for key, view in params.configParser.items("views")]
    error(len(jenkins_views) == 0, "No views", False, RGBLeds.COLOR_YELLOW , "Wrng")

    # Jobs to display
    jenkins_jobs = [job for key, job in params.configParser.items("jobs")]
    error(len(jenkins_jobs) == 0, "No jobs", False, RGBLeds.COLOR_YELLOW , "Wrng")

    error(len(jenkins_jobs) + len(jenkins_jobs) == 0, "No jobs, no views", abort=True)

    # Other parameters
    JenkinsJob.health_period = params.getIntParam("healthperiod", JenkinsJob.health_period)
    JenkinsThread.speed = params.getIntParam("speed", JenkinsThread.speed)  # time in seconds between 2 fetch on the jenkins server
    sleeptime = params.getIntParam("buildboxspeed", 1)                      # delay between 2 display updates

    try:
        # try connecting to the jenkins server, with the URL and credential provided in the ini file
        bl = JenkinsThread(jenkins_url, jenkins_views, jenkins_jobs)
    except jenkinsapi.custom_exceptions as jerr:
        error(True, "Cannot connect to Jenkins", abort=True)

    #get_all_views(bl._bbj._jenkins.views)
    #get_all_jobs(bl._bbj._jenkins.jobs)

    waitmsg="_   "
    while True:
        # TODO later
        # if the 'advance or 'back' button is pressed then skip somme extra builds
        # if <skipButtonPressed>:
        #     bl.skipJobs(1)
        # if <backButtonPressed>:
        #     bl.skipJobs(-1)
        # if <fastforwardButtonPressed>:
        #     bl.skipJobs(10)
        # if <faasBackwardButtonPressed>:
        #     bl.skipJobs(-10)

        bi = bl.getNextBuild()
        if bi == None:
            dd.display(waitmsg)
            waitmsg = waitmsg[3] + waitmsg[:3]
            time.sleep(0.2)
        else:
            #print("Displayaing %s" % bi.name)
            dd.display(STATUS_MSG[bi.last])
            gd.clear()
            gd.displaytext(2, 2, bi.name[:21])
            gd.displaytext(2, 14, bi.name[22:])
            gd.displaytext(2, 26, bi.view)
            gd.displaytext(2, 38, 'Status=%s' % bi.last)
            if bi.health >= 0:  # if health is not unknown
                index = min(int((100 - bi.health) / 20),4)
                gd.displayicon(96, 26, healthiconlist[index])
            ld.display([STATUS_COLOR[h] for h in bi.history])
            time.sleep(sleeptime)


if __name__ == "__main__":
    main()
