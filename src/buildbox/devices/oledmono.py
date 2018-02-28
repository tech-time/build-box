try:
    import Adafruit_GPIO.SPI as SPI
    import Adafruit_SSD1306

    emulate = False
except ImportError:
    print("Import Error while loading GraphicDisplay module. "
          "Using simulator instead.")
    from .emulator import EmulatedSSD1306_128_64 as SSD1306_128_64

    emulate = True

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps


class XYString:
    def __init__(self, string=None, x=0, y=0):
        self.x = x
        self.y = y
        self.string = string

class XYImage:
    def __init__(self, image=None, x=0, y=0):
        self.x = x
        self.y = y
        self.image = image



class GraphicDisplay:
    def __init__(self):
        RST = 25
        DC = 4
        SPI_PORT = 0
        SPI_DEVICE = 0
        if emulate:
            self.disp = SSD1306_128_64()
        else:
            self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC,
                                                        spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))
        self.disp.begin()
        self.disp.clear()
        self.disp.display()
        # self.font = ImageFont.load_default()
        self.font = ImageFont.truetype("arial.ttf", 9, encoding="unic")
        self.width = self.disp.width
        self.height = self.disp.height
        self.strings = []
        self.xystrings = []
        self.xyimages = []
        self.padding = 2
        self.top = self.padding
        self.bottom = self.height - self.padding
        self.image = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)


    def _refresh(self):
        self._render()
        self.disp.image(self.image)
        self.disp.display()

    def _clear_buffer(self):
        self.draw.rectangle((0, 0, self.width - 1, self.height - 1), outline=255, fill=0)

    def _empty_graphic_elements(self):
        self.strings.clear()
        self.xystrings.clear()
        self.xyimages.clear()

    def clear(self):
        self._empty_graphic_elements()
        self._clear_buffer()
        self.disp.clear()
        self._refresh()

    def add_image(self, image_or_path, x=0, y=0, invert=False):
        # add an image to the list of icons on the screen

        if isinstance(image_or_path, Image.Image):
            image = image_or_path
        else:
            raise NotImplementedError("Can only be called with a PIL Image // TODO: implement image loading")

        if invert:
            image = ImageOps.invert(image.convert('L')).convert('1')

        self.xyimages.append(XYImage(image, x, y))
        self._refresh()

    def add_text(self, string, x=0, y=0, font=None, invert=False):
        # add an string at a given x/y position
        self.xystrings.append(XYString(string, x, y))
        self._refresh()

    def print(self, string):  # add a string to the buffer and refresh screen
        self.strings.append(string)
        self._refresh()

    def _render_strings(self):
        current_ypos = self.height
        ascent, descent = self.font.getmetrics()
        font_height = ascent + descent

        for string in self.strings:
            current_ypos -= font_height
            self.draw.text((0, current_ypos), string, font=self.font, fill=255)
            if current_ypos < 0:
                break


    def _render_xyimages(self):
        for xyimage in self.xyimages:
            self.draw.bitmap((xyimage.x, xyimage.y), xyimage.image, fill=255)

    def _render_xystrings(self):
        for xystring in self.xystrings:
            self.draw.text((xystring.x, xystring.y), xystring.string, font=self.font, fill=255)

    def _render(self):
        self._render_strings()   # render text parts
        self._render_xyimages()  # render images (over text, could be used for frames)
        self._render_xystrings()  # render x/y text (over text and frames)
