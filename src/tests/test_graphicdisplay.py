
import pytest

from buildbox.devices import GraphicDisplay
from PIL import ImageFont


def test_charmaxsize():
    maxwidth = 0
    maxheight = 0
    maxwidth_letter = None
    maxheight_letter = None
    # font = ImageFont.load_default()
    font = ImageFont.truetype("arial.ttf", 8, encoding="unic")
    for letter in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789€&éÊË~ç@":
#    for letter in " .!:'":
        width, height = font.getsize(letter)
        if width > maxwidth:
            print("Maxwidth letter: '%s' %d" % (letter, width))
            maxwidth = width
            maxwidth_letter = letter
        if height > maxheight:
            print("Maxheight letter: '%s' %d" % (letter, height))
            maxheight = height
            maxheight_letter = letter
    for spacing in " .!:'":
        width, height = font.getsize(maxwidth_letter + spacing + maxwidth_letter)
        print("spacing: '%s' width: %d" % (spacing,  width - maxwidth*2))



