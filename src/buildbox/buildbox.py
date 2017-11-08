import colorsys
import time
import os

from .ci.jenkinsthread import JenkinsThread, BuildItem
from .devices import DigitalDisplay, GraphicDisplay, RGBLeds
from .conf import BuildboxParameter

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def main():
    print("Hello World!")
    dd = DigitalDisplay()
    gd = GraphicDisplay()
    ld = RGBLeds()

    STATUS_COLOR = {"SUCCESS":   RGBLeds.COLOR_GREEN,   # GREEN
                    "UNSTABLE":  RGBLeds.COLOR_RED,     # YELLOW
                    "FAILURE":   RGBLeds.COLOR_YELLOW,  # RED
                    "NOT_BUILT": RGBLeds.COLOR_GREY,    # GREY
                    "ABORTED":   RGBLeds.COLOR_GREY     # GREY
                    }
    STATUS = {True: "PASS", False: "FAIL"}

    # iconfile = "../../health-icons 32x32.bmp"
    iconfile = "buildbox/ressources/health-icons NB 32x32.bmp"
    healthiconlist = (Image.open(iconfile).crop((  0, 0,  32, 32)),  # No recent builds failed -> health > 80%
                      Image.open(iconfile).crop(( 33, 0,  64, 32)),  # 20-40% of recent builds failed
                      Image.open(iconfile).crop(( 65, 0,  96, 32)),  # 40-60% of recent builds failed
                      Image.open(iconfile).crop(( 97, 0, 128, 32)),  # 60-80% of recent builds failed
                      Image.open(iconfile).crop((129, 0, 160, 32)))  # all recent builds failed (> 80%)

    def error(test, msg, abort=False):
        if test:
            dd.display("Err")
            ld.display_all(RGBLeds.COLOR_RED)
            gd.clear()
            gd.displaytext(2, 2, msg[:21])
            gd.displaytext(2, 14, msg[22:])
            time.sleep(5)
            if abort:
                exit(-1)

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
        gd.displaytext(2, 26, 'Status=%s' % STATUS[step == 0])
        gd.displayicon(72, 26, healthiconlist[int((100 - i * 5) / 20) - 1])

        hue = int(time.time() * 100) % 360
        color_list = []
        for x in range(8):
            offset = x * 360.0 / 16.0
            h = ((hue + offset) % 360) / 360.0
            color_list.append([int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)])
        ld.display(color_list)
        time.sleep(0.1)

    gd.clear()

    gd.displaytext(2, 2, 'Fetching jobs')
    dd.display("....")
    ld.display_all(RGBLeds.COLOR_GREY)

    params = BuildboxParameter(os.path.expanduser('~') + "/.buildbox")
    params.readConfigurationFromIniFile()
    jenkins_url = params.getParam("url")                        # = "https://factory-ixxi.noisy.ratp/jenkins"
    error(jenkins_url == "", "Jenkins URL error", abort=True)

    # jenkins_views=["SDK Calypso", "API_IXXI_1545", "SDK Calypso", "SDK Calypso"]
    jenkins_views = [view for key, view in params.configParser.items("views")]
    error(len(jenkins_views) == 0, "No views", abort=False)


    p = params.getParam("healthperiod")
    if p != "":
        BuildItem.health_period = p

    #try:
        bl = JenkinsThread(jenkins_url, jenkins_views)
    #except jenkinsapi.custom_exceptions as jerr:
    #    error(True, "Cannot connect to Jenkins", abort=True)
    s = params.getParam("speed")  # time in seconds between 2 fetch on the jenkins server
    if s != "":
        bl.speed = int(s)


    while True:
        bi = bl.getNextBuild()
        dd.display(STATUS[bi.last])
        gd.clear()
        gd.displaytext(2, 2, bi.name[:21])
        gd.displaytext(2, 14, bi.name[22:])
        gd.displaytext(2, 26, 'Status=%s' % STATUS[bi.last])
        if bi.health >= 0:  # if health is not unknown
            index = min(int((100 - bi.health) / 20),4)
            #print("health = %d, index = %d"% (bi.health, index) )
            gd.displayicon(72, 26, healthiconlist[index])

        ld.display([STATUS_COLOR[bi.history[h]] for h in bi.history])
        time.sleep(1)


if __name__ == "__main__":
    main()
