import pytest

from buildbox.devices import DigitalDisplay

# TODO: handle test termination (close window or prevent window creation)
def test_digitaldisplay_cannot_be_created_twice():
    dd = DigitalDisplay()
    with pytest.raises(RuntimeError):
        second_dd = DigitalDisplay()
