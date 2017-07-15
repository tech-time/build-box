
try:
    from .leddigits import DigitalDisplay
except ImportError:
    print("Import Error while loading DigitalDisplay module. " 
          "Using simulator instead.")
    from .leddigitssimulator import DigitalDisplay

from .oledmono import GraphicDisplay

__all__ = [DigitalDisplay, GraphicDisplay]
