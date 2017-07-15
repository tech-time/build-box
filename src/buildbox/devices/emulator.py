import threading

from tkinter import Tk, Label
from PIL import ImageTk



class BuildBoxEmulator(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._image = None
        self._panel = None
        self._top = None
        self._tk_image = None
        self.start()

    def run(self):
        self._top = Tk()
        self._top.mainloop()

    def update_graphic_display(self, image):
        self._image = image
        self._tk_image = ImageTk.PhotoImage(self._image)
        #self._panel = PanedWindow()
        if self._panel:
            self._panel.pack_forget()
        self._panel = Label(self._top, image=self._tk_image)
        self._panel.pack(side="bottom", fill="both", expand="yes")
        #self._top.update_idletasks()
        #self._top.update()

bbemu = None

if bbemu is None:
    bbemu = BuildBoxEmulator()


# Emulated version of OLED screen
class EmulatedSSD1306_128_64:
    width = 128
    height = 64

    def __init__(self):
        pass

    def begin(self):
        pass

    def clear(self):
        pass

    def display(self):
        pass

    def image(self):
        return self._image

    def image(self, image):
        bbemu.update_graphic_display(image)
