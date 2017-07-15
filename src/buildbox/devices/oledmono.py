emulate = False
try:
    import Adafruit_GPIO.SPI as SPI
    import Adafruit_SSD1306
except ImportError:
    print("Import Error while loading GraphicDisplay module. " 
          "Using simulator instead.")
    from tkinter import Tk, PhotoImage, Label, PanedWindow
    from PIL import ImageTk
    import threading
    emulate = True

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class SSD1306_128_64(threading.Thread):
    width = 128
    height = 64

    def __init__(self):
        threading.Thread.__init__(self)
        self._image = None
        self._panel = None
        self.start()

    def run(self):
        self._top = Tk()
        self._top.mainloop()

    def begin(self):
        pass

    def clear(self):
        pass

    def display(self):
        pass

    def image(self):
        return self._image

    def image(self, image):
        self._image = image
        self._tkimage = ImageTk.PhotoImage(self._image)
        #self._panel = PanedWindow()
        if self._panel:
            self._panel.pack_forget()
        self._panel = Label(self._top, image=self._tkimage)
        self._panel.pack(side="bottom", fill="both", expand="yes")
        #self._top.update_idletasks()
        #self._top.update()



class GraphicDisplay:
    def __init__(self):
        RST = 25
        DC = 4
        SPI_PORT = 0
        SPI_DEVICE = 0
        if emulate:
            self.disp = SSD1306_128_64()
        else:
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

