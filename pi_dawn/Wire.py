import os

from pi_dawn import app
from pi_dawn import hw
from pi_dawn import wiring_configuration

class Wire:
    def __init__(self, hardware):
        self.hardware = hardware

    def solder(self):
        return self.hardware
    
    def connect(self, configuration, *args, **kwargs):
        return Wire(configuration(*args, hardware=self.hardware, **kwargs))
    
    def gamma(self, *args, **kwargs):
        return self.connect(wiring_configuration.GammaCorrection, *args, **kwargs)
    
    def bayer(self, *args, **kwargs):
        return self.connect(wiring_configuration.BayerCorrection, *args, **kwargs)
    
    def debug(self, *args, **kwargs):
        return self.connect(wiring_configuration.Debug, *args, **kwargs)
    
    def alternate(self, *args, **kwargs):
        return self.connect(wiring_configuration.Alternate, *args, **kwargs)

    def strip(self, *args, **kwargs):
        return self.connect(wiring_configuration.Strip, *args, **kwargs)

if os.environ.get('DEBUG', '0') == '1':
    device = Wire(hw.Pygame(width=10, height=32))
else:
    device = (Wire(hw.WS2801(length=320)).strip(32).alternate())

wired = (device
        .debug(False)
        .bayer()
        .gamma()
        .solder())
