import pytest

from buildbox.devices import DigitalDisplay

def test_digitaldisplay_cannot_created_twice():
    dd = DigitalDisplay()
    with pytest.raises(RuntimeError):
        econd_dd= DigitalDisplay()
