import attr
from typing import Tuple, NewType

from .Color import Color
from .Geometry import Geometry


Pixel = NewType('Pixel', Tuple[int, int])

@attr.s(init=False)
class Surface:
    def __init__(self, screen):
        self.width = screen.width
        self.height = screen.height
        self.data = self.width * self.height * [Color(0, 0, 0)]

    def get_pixel(self, x, y):
        offset = y * self.width + x

        return self.data[offset]
    
    def set_pixel(self, pixel: Pixel, color: Color):
        x, y = pixel
        offset = y * self.width + x
        self.data[offset] = color

        return self

    def draw(self, drawing: Geometry):
        drawing.draw(self)

        return self
