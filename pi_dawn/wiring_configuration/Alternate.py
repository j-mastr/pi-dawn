from pi_dawn.hw import Hardware
from pi_dawn.wiring_configuration.WiringConfigurationDecorator import WiringConfigurationDecorator

class Alternate(WiringConfigurationDecorator):
    def __init__(self, height, hardware: Hardware = None):
        super().__init__(hardware)
        self.height = height

    def set_pixel(self, screen, pixel, color):
        x, y = pixel
        if x % 2 == 0:
            y = self.height - y - 1

        self.hardware.set_pixel(screen, (x, y), color)
