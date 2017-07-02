from .devices import DigitalDisplay
import time

def main():
    print("Hello World!")
    dd = DigitalDisplay()
    while(1):
        dd.display('COOL')
        time.sleep(0.5)
        dd.display('dudE')
        time.sleep(0.5)


if __name__ == "__main__":
    # execute only if run as a script
    main()
