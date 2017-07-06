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
        time.sleep(0.5)
        dd.display('dUdE')
        time.sleep(0.5)


if __name__ == "__main__":
    main()
