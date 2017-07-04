from .devices import DigitalDisplay, GraphicDisplay
import time

def main():
    print("Hello World!")
    dd = DigitalDisplay()
    gd = GraphicDisplay()
    gd.displaytext(2,2, "Cool Dude!")
    gd.clear()
    gd.displaytext(2,2, "Dude Cool!")
    i = 0
    while(1):
        dd.display('COOL')
        time.sleep(0.5)
        dd.display('dudE')
        time.sleep(0.5)
        i += 1
        if i  > 5:
            break


if __name__ == "__main__":
    # execute only if run as a script
    main()
