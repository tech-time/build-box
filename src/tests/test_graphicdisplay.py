
import pytest

from buildbox.devices import GraphicDisplay
from PIL import ImageFont

# Refs:
# https://stackoverflow.com/questions/43060479/how-to-get-the-font-pixel-height-using-pil-imagefont
# https://pillow.readthedocs.io/en/3.0.0/_modules/PIL/ImageFont.html
# https://github.com/python-pillow/Pillow/issues/1660
# https://github.com/python-pillow/Pillow/issues/1646
def test_charmaxsize():
    maxwidth = 0
    maxheight = 0
    maxwidth_letter = None
    maxheight_letter = None
    # font = ImageFont.load_default()
    font = ImageFont.truetype("arial.ttf", 9, encoding="unic")
    print("XXXXX: "+ str(font.getmetrics()))
    for letter in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789€&éÊË~ç@":
#    for letter in " .!:'":
        width, height = font.getsize(letter)
        (width2, baseline), (offset_x, offset_y) = font.font.getsize(letter)
        # try font.getmask(text).getbbox()
        if width > maxwidth:
            print("Maxwidth letter: '%s' %d  / %d %d - %d %d" % (letter, width, width2, baseline, offset_x, offset_y))
            maxwidth = width
            maxwidth_letter = letter
        if height > maxheight or letter in "ÊE":
            print("Maxheight letter: '%s' %d  / %d %d - %d %d" % (letter, height, width2, baseline, offset_x, offset_y))
            maxheight = height
            maxheight_letter = letter
    for spacing in " .!:'":
        width, height = font.getsize(maxwidth_letter + spacing + maxwidth_letter)
        print("spacing: '%s' width: %d" % (spacing,  width - maxwidth*2))



