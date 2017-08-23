
try:
    from .leddigits import DigitalDisplay
except ImportError:
    print("Import Error while loading DigitalDisplay module. " 
          "Using simulator instead.")
    from .leddigitssimulator import DigitalDisplay

from .oledmono import GraphicDisplay

try:
    from .ledbar import LEDDisplay
except ImportError:
    print("Import Error while loading LEDDisplay module. " 
          "Using simulator instead.")
    from .ledbarsimulator import LEDDisplaySimulator as LEDDisplay

__all__ = [DigitalDisplay, GraphicDisplay, LEDDisplay]
