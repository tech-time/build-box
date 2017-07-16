import threading

from tkinter import Tk, Label, StringVar
from tkinter.font import Font
from PIL import ImageTk



class BuildBoxEmulator(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._image = None
        self._panel = None
        self._tk_image = None
        self._top = None
        self._digital_display_value = None
        self.start()

    def run(self):
        self._top = Tk()
        self._digital_display_value = StringVar()
        self._digital_display_value.set("42.17")
        # cf. https://www.google.fr/search?q=digital+7+ttf
        myFont = Font(family="Digital-7", size=42)  # ,  weight="bold")
        label = Label(self._top, textvariable=self._digital_display_value, font=myFont, fg="red", bg="black")
        label.pack()
        self._top.mainloop()

    def update_digital_display(self, string):
        self._digital_display_value.set(string)

    def update_graphic_display(self, image):
        self._image = image
        self._tk_image = ImageTk.PhotoImage(self._image)
        if self._panel is None:
            self._panel = Label(self._top, image=self._tk_image)
            self._panel.pack(side="bottom", fill="both", expand="yes")
        else:
            self._panel.configure(image=self._tk_image)

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
