from threading import Thread
import atexit
import Pi7SegPy as pi7seg

class DigitalDisplay(Thread):

    __initialized_once = False
    __EMPTY_DISPLAY = None

    def __init__(self, data_pin=5,clock_pin=13,latch_pin=6,
                    registers=2, no_of_displays=4,
                    common_cathode_type=True):

        # Until Pi7SegPy is refactored, class can only be instanciated once
        if DigitalDisplay.__initialized_once is True:
            raise RuntimeError("Digital Display can only be instanciated once")
        else:
            DigitalDisplay.__initialized_once = True

        super().__init__(daemon=True)

        pi7seg.init(data_pin, clock_pin,latch_pin,
                     registers,no_of_displays, common_cathode_type)

        atexit.register( self.clear_display )
        self.name = 'DigitalDisplay Thread'
        self.__EMPTY_DISPLAY = [ ' ' ] * no_of_displays
        self.__chars_to_display = list(self.__EMPTY_DISPLAY)
        self.start()


    def clear_display(self):
        self.__chars_to_display = list(self.__EMPTY_DISPLAY)
        pi7seg.show(self.__EMPTY_DISPLAY)


    def run(self):
        while True:
            pi7seg.show(self.__chars_to_display)


    def display(self, value):
        self.__chars_to_display = list(value)
