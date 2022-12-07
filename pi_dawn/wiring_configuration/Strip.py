import math

from pi_dawn.hw import Hardware
from pi_dawn.graphics import Color
from pi_dawn.wiring_configuration.WiringConfigurationDecorator import WiringConfigurationDecorator

class Strip(WiringConfigurationDecorator):
    def __init__(self, height, hardware: Hardware = None):
        super().__init__(hardware)
        self.height = height

    def set_pixel(self, screen, pixel, color: Color):
        x, y = pixel
        self.hardware.set_pixel(screen, (y + x * self.height, 0), color)

    def get_dimensions(self):
        width, height = self.hardware.get_dimensions()
        return (math.ceil(width / self.height), self.height)
