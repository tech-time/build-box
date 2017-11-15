#
#
#



rgbledsemulate = False

try:
    # import needed to access the real blinkt display
    import blinkt
except ImportError:
    # if not there use alternative graphic emulator
    from .emulator import bbemu
    rgbledsemulate = True


class RGBLeds():
    NUM_PIXELS = 8  # Number of pixel
    BRIGHTNESS = 0.5  # Default brightness  (value from 0.0 to 1.0), used for blinkt only

    COLOR_GREEN     = (  0, 255,   0)  # GREEN
    COLOR_YELLOW    = (255, 255,   0)  # YELLOW
    COLOR_RED       = (255,   0,   0)  # RED
    COLOR_GREY      = (128, 128, 128)  # GREY
    COLOR_BLACK     = (  0,   0,   0)  # BLACK = all leds off

    ALL_OFF = [COLOR_BLACK] * NUM_PIXELS

    __initialized_once = False

    def __init__(self):
        if self.__initialized_once is True:
            raise RuntimeError("Digital Display can only be instanciated once")
        else:
            self.colors = RGBLeds.ALL_OFF.copy()
            self.__initialized_once = True

    def clear(self):
        """Clear the pixel buffer"""
        self.colors = RGBLeds.ALL_OFF.copy()
        if rgbledsemulate:
            bbemu.update_led_display(self)
        else:
            blinkt.clear()

    def display(self, color_list):
        self.colors = (color_list + RGBLeds.ALL_OFF)[:RGBLeds.NUM_PIXELS]
        if rgbledsemulate:
            bbemu.update_led_display(self)
        else:
            for i in range(RGBLeds.NUM_PIXELS):
                r, g, b = self.colors[i]
                blinkt.set_pixel(i, r, g, b, RGBLeds.BRIGHTNESS)
            blinkt.show()

    def display_all(self, color):
        self.display([color] * RGBLeds.NUM_PIXELS)
