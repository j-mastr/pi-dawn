from pi_dawn.hw import Hardware
from pi_dawn.graphics import Color
from pi_dawn.wiring_configuration.WiringConfigurationDecorator import WiringConfigurationDecorator

class BayerCorrection(WiringConfigurationDecorator):
    def __init__(self, hardware: Hardware = None):
        super().__init__(hardware)
        self.bayer_map = self.build_bayer_map()

    def set_pixel(self, screen, pixel, color: Color):
        x, y = pixel
        r, g, b = color

        t = self.bayer_map[y % 2][x % 2]
        c = Color(*[max(0, min(255, round(c + t))) for c in color])
        
        self.hardware.set_pixel(screen, pixel, c)

    @staticmethod
    def build_bayer_map():
        map = [
            [0.0, 2.0],
            [3.0, 1.0],
        ]
        for x in range(2):
            for y in range(2):
                map[y][x] = 0.5 * map[y][x] - 1.0
        return map
