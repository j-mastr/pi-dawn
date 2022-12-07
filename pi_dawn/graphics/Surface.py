import attr

from .Color import Color


@attr.s(init=False)
class Surface:
    def __init__(self, screen):
        self.width = screen.width
        self.height = screen.height
        self.data = self.width * self.height * [Color(0, 0, 0)]

    def get_pixel(self, x, y):
        offset = y * self.width + x

        return self.data[offset]
    
    def set_pixel(self, pixel, color: Color):
        x, y = pixel
        offset = y * self.width + x
        self.data[offset] = color

        return self

    def draw(self, drawing):
        drawing.draw(self)

        return self
