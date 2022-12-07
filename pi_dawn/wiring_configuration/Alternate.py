from pi_dawn.graphics import Color
from pi_dawn.wiring_configuration.WiringConfigurationDecorator import WiringConfigurationDecorator

class Alternate(WiringConfigurationDecorator):
    def set_pixel(self, screen, pixel, color: Color):
        width, height = self.hardware.get_dimensions()
        x, y = pixel
        if x % 2 == 0:
            y = height - y - 1

        self.hardware.set_pixel(screen, (x, y), color)
