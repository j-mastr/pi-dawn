import attr
import pygame

from pi_dawn import graphics


@attr.s(init=False)
class Screen:
    width = attr.ib(type=int)
    height = attr.ib(type=int)
    hardware = attr.ib()

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set_hardware(self, hardware):
        self.hardware = hardware

    def make_surface(self):
        return graphics.Surface(self)

    def draw_surface(self, surface):
        self.hardware.start_refresh()
        self.set_pixels(surface)
        self.hardware.refresh()
    
    def set_pixels(self, surface):
        for y in range(surface.height):
            for x in range(surface.width):
                self.hardware.set_pixel((x,y), surface.get_pixel(x, y))
