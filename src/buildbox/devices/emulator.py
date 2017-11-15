import threading

from tkinter import Tk, Label, StringVar, Canvas
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

        # Added: Graphic display for 7Led display (blinkt)
        self._led_canvas = None
        self.start()

    def run(self):
        self._top = Tk()
        self._digital_display_value = StringVar()
        self._digital_display_value.set("42.17")
        # cf. https://www.google.fr/search?q=digital+7+ttf
        # myFont = Font(family="Digital-7", size=42)  # ,  weight="bold")
        # cf. https://fontlibrary.org/en/font/segment7
        segments_font = Font(family="Segment7", size=42)  # ,  weight="bold")
        label = Label(self._top, textvariable=self._digital_display_value, font=segments_font, fg="red", bg="black")
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

    # Update LED display
    def update_led_display(self, ld):
        LED_SIZE = 25
        LED_SPACER = 3
        LED_NUMBER = len(ld.colors)
        WIDTH = (LED_SIZE + LED_SPACER) * LED_NUMBER + LED_SPACER
        HEIGHT = LED_SIZE + LED_SPACER * 2
        if self._led_canvas is None:
            self._led_canvas = Canvas(self._top, width=WIDTH, height=HEIGHT)
            self._led_canvas.pack()
        self._led_canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="blue")
        x = LED_SPACER + 1  # x position of the led
        for (r, g, b) in ld.colors:
            self._led_canvas.create_rectangle(x, LED_SPACER, x + LED_SIZE, LED_SIZE + LED_SPACER,
                                              fill='#%02x%02x%02x' % (r, g, b))
            x = x + LED_SIZE + LED_SPACER


if 'bbemu' not in globals():
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

    def image(self, image):
        bbemu.update_graphic_display(image)
