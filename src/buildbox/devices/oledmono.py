import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class GraphicDisplay:
    def __init__(self):
        RST = 25
        DC = 4
        SPI_PORT = 0
        SPI_DEVICE = 0
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))
        self.disp.begin()
        self.disp.clear()
        self.disp.display()
        self.font = ImageFont.load_default()
        self.width = self.disp.width
        self.height = self.disp.height
        self.padding = 2
        self.top = self.padding
        self.bottom = self.height-self.padding
        self.image = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)

    def displaytext(self, x, y, text):
        self.draw.text((x, y),   text,  font=self.font, fill=255)
        self.refresh()

    def refresh(self):
        self.disp.image(self.image)
        self.disp.display()

    def clear(self):
        self.draw.rectangle((0, 0, self.width-1, self.height-1), outline=255, fill=0)
        self.disp.clear()
        self.refresh()

