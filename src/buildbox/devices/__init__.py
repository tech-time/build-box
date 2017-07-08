
try:
    from .leddigits import DigitalDisplay
except ImportError:
    print("Import Error while loading DigitalDisplay module. " 
          "Using simulator instead.")
    from .leddigitssimulator import DigitalDisplay

try:
    from .oledmono import GraphicDisplay
except ImportError:
    GraphicDisplay = None

__all__ = [DigitalDisplay, GraphicDisplay]
