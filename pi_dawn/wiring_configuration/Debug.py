import os
import time

from pi_dawn.hw import Hardware
from pi_dawn.wiring_configuration.WiringConfigurationDecorator import WiringConfigurationDecorator

class Debug(WiringConfigurationDecorator):
    def __init__(self, debug: bool = os.environ.get('DEBUG', '0') == '1', hardware: Hardware = None):
        super().__init__(hardware)
        self.debug = debug
        self.state = StateDebug(self.hardware) if debug else StateProduction(self.hardware)

    def start_refresh(self):
        self.state.start_refresh()

    def refresh(self):
        self.state.refresh()

    def set_pixel(self, screen, pixel, color):
        self.state.set_pixel(screen, pixel, color)

class StateDebug:
    def __init__(self, hardware):
        self.hardware = hardware

    def start_refresh(self):
        pass

    def refresh(self):
        pass

    def set_pixel(self, screen, pixel, color):
        self.hardware.start_refresh()
        self.hardware.set_pixel(screen, pixel, color)
        self.hardware.refresh()

        time.sleep(0.05)

class StateProduction:
    def __init__(self, hardware):
        self.hardware = hardware

    def start_refresh(self):
        self.hardware.start_refresh()

    def refresh(self):
        self.hardware.refresh()

    def set_pixel(self, screen, pixel, color):
        self.hardware.set_pixel(screen, pixel, color)
