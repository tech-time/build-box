from .devices import DigitalDisplay, GraphicDisplay

import time


def main():
    print("Hello World!")
    dd = DigitalDisplay()
    gd = GraphicDisplay()
    gd.displaytext(2, 2, "Cool Dude!")
    gd.clear()
    gd.displaytext(2, 2, "Dude Cool!")

    while True:
        dd.display('COOL')
        gd.clear()
        gd.displaytext(2, 2, "Dude Cool!")
        time.sleep(0.5)
        dd.display('dudE')
        gd.clear()
        gd.displaytext(2, 2, "Cool Dude!")
        time.sleep(0.5)


if __name__ == "__main__":
    main()
