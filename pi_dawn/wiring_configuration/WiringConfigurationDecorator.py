from pi_dawn.hw import Hardware

class WiringConfigurationDecorator(Hardware):
    def __init__(self, hardware: Hardware = None):
        self.hardware = hardware

    def decorate(self, hardware: Hardware):
        self.hardware = hardware

    def start_refresh(self):
        self.hardware.start_refresh()

    def refresh(self):
        self.hardware.refresh()

    def set_pixel(self, screen, pixel, color):
        self.hardware.set_pixel(screen, pixel, color)

    def get_dimensions(self):
        return self.hardware.get_dimensions()
