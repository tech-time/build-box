from .devices import DigitalDisplay, GraphicDisplay, RGBLeds

import time
import colorsys

from .continuousintegration import Jobs


def main():
    print("Hello World!")
    dd = DigitalDisplay()
    gd = GraphicDisplay()
    ld = RGBLeds()

    spacing = 360.0 / 16.0
    ld.set_brightness(0.1)

    step = 1
    for i in range(10):
        gd.clear()
        if step == 0:
            gd.displaytext(2, 2, "Dude Cool!")
            dd.display('dudE')
        else:
            gd.displaytext(2, 2, "Cool Dude!")
            dd.display('COOL')
        step = (step + 1) % 2

        hue = int(time.time() * 100) % 360
        for x in range(8):
            offset = x * spacing
            h = ((hue + offset) % 360) / 360.0
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
            ld.set_pixel(x, r, g, b)
        ld.show()
        time.sleep(0.5)

    bl = Jobs()
    while True:
        bi = bl.getnextbuild()
        dd.display(bi.name)
        gd.clear()
        gd.displaytext(2, 2, 'Job: ' + bi.name)
        gd.displaytext(2, 22, 'H=%s' % bi.health)
        gd.displaytext(2, 42, 'S=%s' % bi.status)

        if 0 <= bi.status <= 50:
            r, g, b = 255,   0,  0
        if 51 <= bi.status <= 80:
            r, g, b = 255, 128, 64
        if 81 <= bi.status <= 99:
            r, g, b = 0, 255,  0

        ld.clear()
        for x in range(8):
            if (bi.status/100) > (x/8):
                ld.set_pixel(x, r, g, b)
        ld.displayleds()

        time.sleep(1)


if __name__ == "__main__":
    main()
