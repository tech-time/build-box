from threading import Thread
import atexit
import time
from .emulator import bbemu


class DigitalDisplay(Thread):

    __initialized_once = False
    __EMPTY_DISPLAY = None

    def __init__(
            self, data_pin=None, clock_pin=None, latch_pin=None,
            registers=None, no_of_displays=4,
            common_cathode_type=None):

        # Until Pi7SegPy is refactored, class can only be instanciated once
        if DigitalDisplay.__initialized_once is True:
            raise RuntimeError("Digital Display can only be instanciated once")
        else:
            DigitalDisplay.__initialized_once = True

        super().__init__(daemon=True)

        atexit.register( self.clear_display )
        self.name = 'DigitalDisplay Thread'
        self.__EMPTY_DISPLAY = ' ' * no_of_displays
        self.__chars_to_display = self.__EMPTY_DISPLAY
        self.start()

    def clear_display(self):
        self.__chars_to_display = self.__EMPTY_DISPLAY
        print(self.__EMPTY_DISPLAY)

    def run(self):
        last_displayed = None
        while True:
            if self.__chars_to_display != last_displayed:
                last_displayed = self.__chars_to_display
                print("7SEG: " + self.__chars_to_display)
                bbemu.update_digital_display(self.__chars_to_display)
            time.sleep(0.05)

    def display(self, value):
        self.__chars_to_display = value
