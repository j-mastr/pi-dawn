from pi_dawn.hw import Hardware
from pi_dawn.graphics import Color
from pi_dawn.wiring_configuration.WiringConfigurationDecorator import WiringConfigurationDecorator
from pi_dawn import app

class GammaCorrection(WiringConfigurationDecorator):
    def __init__(self, hardware: Hardware = None, gamma_r=app.config['GAMMA_R'], gamma_g=app.config['GAMMA_G'], gamma_b=app.config['GAMMA_B']):
        super().__init__(hardware)

        self.lut = [
            self.build_gamma_lut(gamma_r),
            self.build_gamma_lut(gamma_g),
            self.build_gamma_lut(gamma_b),
        ]

    def set_pixel(self, screen, pixel, color: Color):
        withGamma = [self.lut[index][c] if len(self.lut) > index else c for index, c in enumerate(color)]
        self.hardware.set_pixel(screen, pixel, Color(*withGamma))

    @staticmethod
    def build_gamma_lut(g):
        inverse_g = 1 / g
        return [255 * ((i / 255) ** inverse_g) for i in range(256)]
