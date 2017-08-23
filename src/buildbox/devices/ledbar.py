'''
Blinkt 7 LED display module from PImoroni

Adapted from the blinkt module available on https://github.com/pimoroni/blinkt

'''


try:
    # import needed to access the real blinkt display
    import RPi.GPIO as GPIO
    import atexit
except ImportError:
    #if not there use alternative graphic emulator
    import LEDDisplaySimulator as LEDDisplay




class LEDDisplay():
    DAT = 23        # GPIO pin for Data transmission
    CLK = 24        # GPIO pin for CLK signal
    NUM_PIXELS = 8  # Number of pixel
    BRIGHTNESS = 7  # Default brightness  (value from 0 to 31)

    # Then actual pixel internal storage : 8 RGB LEDs
    pixels = [[0, 0, 0, BRIGHTNESS]] * NUM_PIXELS

    _gpio_setup = False     # Flag to indicate that the GPIO setup was already done
    _clear_on_exit = True   # Should the display be cleared on exit ?

    def __init__(self):
        atexit.register(self._exit)     # Register the exit procedure (clears display and close GPIO

    def _exit(self):
        if self._clear_on_exit:
            self.clear()
            self.how()
        GPIO.cleanup()


    def set_brightness(self, brightness):
        """Set the brightness of all pixels

        :param brightness: Brightness: 0.0 to 1.0
        """
        if brightness < 0 or brightness > 1:
            raise ValueError("Brightness should be between 0.0 and 1.0")

        for x in range(self.NUM_PIXELS):
            self.pixels[x][3] = int(31.0 * brightness) & 0b11111

    def clear(self):
        """Clear the pixel buffer"""
        for x in range(self.NUM_PIXELS):
            self.pixels[x][0:3] = [0, 0, 0]

    def _write_byte(self, byte):
        for x in range(8):
            GPIO.output(self.DAT, byte & 0b10000000)
            GPIO.output(self.CLK, 1)
            byte <<= 1
            GPIO.output(self.CLK, 0)

    # Emit exactly enough clock pulses to latch the small dark die APA102s which are weird
    # for some reason it takes 36 clocks, the other IC takes just 4 (number of pixels/2)
    def _eof(self):
        GPIO.output(self.DAT, 0)
        for x in range(36):
            GPIO.output(self.CLK, 1)
            GPIO.output(self.CLK, 0)

    def _sof(self):
        GPIO.output(self.DAT, 0)
        for x in range(32):
            GPIO.output(self.CLK, 1)
            GPIO.output(self.CLK, 0)

    def show(self):
        """Output the buffer to Blinkt!"""

        if not self._gpio_setup:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(self.DAT, GPIO.OUT)
            GPIO.setup(self.CLK, GPIO.OUT)
            self._gpio_setup = True

            self._sof()

        for pixel in self.pixels:
            r, g, b, brightness = pixel
            self._write_byte(0b11100000 | brightness)
            self._write_byte(b)
            self._write_byte(g)
            self._write_byte(r)
            self._eof()

    def set_all(self, r, g, b, brightness=None):
        """Set the RGB value and optionally brightness of all pixels

        If you don't supply a brightness value, the last value set for each pixel be kept.

        :param r: Amount of red: 0 to 255
        :param g: Amount of green: 0 to 255
        :param b: Amount of blue: 0 to 255
        :param brightness: Brightness: 0.0 to 1.0 (default around 0.2)
        """
        for x in range(self.NUM_PIXELS):
            self.set_pixel(x, r, g, b, brightness)

    def get_pixel(self,x):
        """Get the RGB and brightness value of a specific pixel"""

        r, g, b, brightness = self.pixels[x]
        brightness /= 31.0
        return r, g, b, round(brightness, 3)

    def set_pixel(self, x, r, g, b, brightness=None):
        """Set the RGB value, and optionally brightness, of a single pixel

        If you don't supply a brightness value, the last value will be kept.

        :param x: The horizontal position of the pixel: 0 to 7
        :param r: Amount of red: 0 to 255
        :param g: Amount of green: 0 to 255
        :param b: Amount of blue: 0 to 255
        :param brightness: Brightness: 0.0 to 1.0 (default around 0.2)
        """
        if brightness is None:
            brightness = self.pixels[x][3]
        else:
            brightness = int(31.0 * brightness) & 0b11111

        self.pixels[x] = [int(r) & 0xff, int(g) & 0xff, int(b) & 0xff, brightness]

    def set_clear_on_exit(self, value=True):
        """Set whether Blinkt! should be cleared upon exit

        By default Blinkt! will turn off the pixels on exit, but calling::

            blinkt.set_clear_on_exit(False)

        Will ensure that it does not.

        :param value: True or False (default True)
        """
        self._clear_on_exit = value





