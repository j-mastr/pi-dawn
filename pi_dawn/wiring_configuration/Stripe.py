from pi_dawn.wiring_configuration.WiringConfigurationDecorator import WiringConfigurationDecorator

class Stripe(WiringConfigurationDecorator):
    def set_pixel(self, screen, pixel, color):
        x, y = pixel
        self.hardware.set_pixel(screen, (y + x * screen.height, 0), color)
