import time
import colorsys

from .ci.jenkinsthread import JenkinsThread, JenkinsJob

from .devices import DigitalDisplay, GraphicDisplay, RGBLeds
from .conf import BuildboxConfig

from PIL import Image

dd = DigitalDisplay()
gd = GraphicDisplay()
ld = RGBLeds()

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
    params = BuildboxConfig()
    params.readConfigurationFromIniFile()

    sleeptime = params.getIntParam("buildboxspeed", 1)  # delay between 2 display updates
    ci_server = init_ci_server(params)

    waitmsg="_   "
    while True:
        # TODO later
        # if the 'advance or 'back' button is pressed then skip somme extra builds
        # if <skipButtonPressed>:
        #     ci_server.skipJobs(1)
        # if <backButtonPressed>:
        #     ci_server.skipJobs(-1)
        # if <fastforwardButtonPressed>:
        #     ci_server.skipJobs(10)
        # if <faasBackwardButtonPressed>:
        #     ci_server.skipJobs(-10)

        build = ci_server.getNextBuild()
        if build is None:
            dd.display(waitmsg)
            waitmsg = waitmsg[3] + waitmsg[:3]
            time.sleep(0.2)
        else:
            dd.display(STATUS_MSG[build.last])
            gd.clear()
            gd.displaytext(2, 2, build.name[:21])
            gd.displaytext(2, 14, build.name[22:])
            gd.displaytext(2, 26, build.view)
            gd.displaytext(2, 38, 'Status=%s' % build.last)
            if build.health >= 0:  # if health is not unknown
                index = min(int((100 - build.health) / 20),4)
                gd.displayicon(96, 26, healthiconlist[index])
            ld.display([STATUS_COLOR[h] for h in build.history])
            time.sleep(sleeptime)


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


def init_ci_server(params):
    # Jenkins server URL
    jenkins_url = params.getParam("url")  # = "https://xxxxxxx/jenkins"
    error(jenkins_url == "", "Jenkins URL error", abort=True)
    # Views to display
    jenkins_views = [view for key, view in params.configParser.items("views")]
    error(len(jenkins_views) == 0, "No views", False, RGBLeds.COLOR_YELLOW, "Wrng")
    # Jobs to display
    jenkins_jobs = [job for key, job in params.configParser.items("jobs")]
    error(len(jenkins_jobs) == 0, "No jobs", False, RGBLeds.COLOR_YELLOW, "Wrng")
    error(len(jenkins_jobs) + len(jenkins_jobs) == 0, "No jobs, no views", abort=True)
    # Other parameters
    JenkinsJob.health_period = params.getIntParam("healthperiod", JenkinsJob.health_period)
    JenkinsThread.speed = params.getIntParam("speed",
                                             JenkinsThread.speed)  # time in seconds between 2 fetch on the jenkins server
    try:
        # try connecting to the jenkins server, with the URL and credential provided in the ini file
        ci_server = JenkinsThread(jenkins_url, jenkins_views, jenkins_jobs)
    except Exception as err:
        error(True, "Problem during Jenkins thread creation: %s" % err, abort=True)
    return ci_server


if __name__ == "__main__":
    main()
