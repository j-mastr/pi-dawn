import attr

import Adafruit_WS2801
import Adafruit_GPIO.SPI

from pi_dawn import graphics
from pi_dawn.graphics import Color
from pi_dawn.hw.Hardware import Hardware

SPI_PORT = 0
SPI_DEVICE = 0


@attr.s(init=False)
class WS2801(Hardware):
    length = attr.ib(type=int)

    def __init__(self, length):
        self.length = length

        self.pixels = Adafruit_WS2801.WS2801Pixels(length, spi=Adafruit_GPIO.SPI.SpiDev(SPI_PORT, SPI_DEVICE))

    def set_pixel(self, screen, pixel, color: Color):
        offset, y = pixel
        self.pixels.set_pixel_rgb(offset, *color)

    def refresh(self):
        self.pixels.show()

    def get_dimensions(self):
        return (self.length, 1)
