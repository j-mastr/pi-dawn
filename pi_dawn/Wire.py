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

    def stripe(self, *args, **kwargs):
        return self.connect(wiring_configuration.Stripe, *args, **kwargs)

if os.environ.get('DEBUG', '0') == '1':
    wired = hw.Pygame(width=10, height=32)
else:
    wired = hw.WS2801(width=10, height=32, gamma_r=app.config['GAMMA_R'], gamma_b=app.config['GAMMA_B'],
                    gamma_g=app.config['GAMMA_G'])
