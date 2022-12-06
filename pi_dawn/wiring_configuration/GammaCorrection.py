from pi_dawn.hw import Hardware
from pi_dawn.wiring_configuration.WiringConfigurationDecorator import WiringConfigurationDecorator

class GammaCorrection(WiringConfigurationDecorator):
    def __init__(self, hardware: Hardware = None, gamma_r=2, gamma_g=2, gamma_b=2):
        self.hardware = hardware

        self.lut_r = self.build_gamma_lut(gamma_r)
        self.lut_g = self.build_gamma_lut(gamma_g)
        self.lut_b = self.build_gamma_lut(gamma_b)

    def set_pixel(self, screen, pixel, color):
        r, g, b = color
        r, g, b = self.lut_r[r], self.lut_g[g], self.lut_b[b]

        self.hardware.set_pixel(screen, pixel, (r, g, b))

    @staticmethod
    def build_gamma_lut(g):
        inverse_g = 1 / g
        return [255 * ((i / 255) ** inverse_g) for i in range(256)]
