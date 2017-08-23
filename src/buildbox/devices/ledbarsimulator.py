
from .emulator import bbemu

class LEDDisplaySimulator():
    NUM_PIXELS = 8  # Number of pixel
    BRIGHTNESS = 7  # Default brightness  (value from 0 to 31)

    # Then actual pixel internal storage : 8 RGB LEDs
    pixels = [[0, 0, 0, BRIGHTNESS]] * NUM_PIXELS

    __initialized_once = False

    def __init__(self):
        if self.__initialized_once is True:
            raise RuntimeError("Digital Display can only be instanciated once")
        else:
            self.__initialized_once = True


    def set_brightness(self, brightness):
        """Set the brightness of all pixels

        :param brightness: Brightness: 0.0 to 1.0
        """
        if brightness < 0 or brightness > 1:
            raise ValueError("Brightness should be between 0.0 and 1.0")
        for x in range(LEDDisplaySimulator.NUM_PIXELS):
            self.pixels[x][3] = int(31.0 * brightness) & 0b11111

    def clear(self):
        """Clear the pixel buffer"""
        for x in range(self.NUM_PIXELS):
            self.pixels[x][0:3] = [0, 0, 0]

    def show(self):
        # Sends the pixel to the BuilbBox emulator for displaying
        bbemu.update_led_display(self)

    def set_all(self, r, g, b, brightness=None):
        """Set the RGB value and optionally brightness of all pixels

        If you don't supply a brightness value, the last value set for each pixel be kept.

        :param r: Amount of red: 0 to 255
        :param g: Amount of green: 0 to 255
        :param b: Amount of blue: 0 to 255
        :param brightness: Brightness: 0.0 to 1.0 (default around 0.2)
        """
        for x in range(self.NUM_PIXELS):
            self.set_pixel( x, r, g, b, brightness)

    def get_pixel(self, x):
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
        # just ignore
        pass

