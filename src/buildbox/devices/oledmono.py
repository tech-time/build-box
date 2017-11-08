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
        self.font = ImageFont.load_default()
        self.width = self.disp.width
        self.height = self.disp.height
        self.padding = 2
        self.top = self.padding
        self.bottom = self.height - self.padding
        self.image = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)

    def displaytext(self, x, y, text):
        self.draw.text((x, y), text, font=self.font, fill=255)
        self.refresh()

    def displayicon(self, x, y, icon):
        # inverts the given icon and convert the result in black&white icon before pasting the icon in the image
        self.draw.bitmap((x, y), ImageOps.invert(icon.convert('L')).convert('1'), fill=255)
        self.refresh()

    def refresh(self):
        self.disp.image(self.image)
        self.disp.display()

    def clear(self):
        self.draw.rectangle((0, 0, self.width - 1, self.height - 1), outline=255, fill=0)
        self.disp.clear()
        self.refresh()
