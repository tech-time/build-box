from .devices import DigitalDisplay, GraphicDisplay, LEDDisplay

import time
import colorsys

def main():
    print("Hello World!")
    dd = DigitalDisplay()
    gd = GraphicDisplay()
    ld = LEDDisplay()

    spacing = 360.0 / 16.0
    hue = 0
    ld.set_brightness(0.1)

    step=1
    while True:
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


if __name__ == "__main__":
    main()
