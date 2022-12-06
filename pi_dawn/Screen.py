import attr
import pygame

from pi_dawn import graphics


@attr.s(init=False)
class Screen:
    width = attr.ib(type=int)
    height = attr.ib(type=int)
    hardware = attr.ib()
    abort = attr.ib()

    def __init__(self, width, height, hardware):
        self.width = width
        self.height = height
        self.hardware = hardware

    def set_hardware(self, hardware):
        self.hardware = hardware

    def make_surface(self):
        return graphics.Surface(self)

    def draw_surface(self, surface):
        self.abort = False
        self.hardware.start_refresh()
        self.set_pixels(surface)
        self.hardware.refresh()
    
    def set_pixels(self, surface):
        for y in range(surface.height):
            for x in range(surface.width):
                if self.abort:
                    break
                self.hardware.set_pixel(self, (x,y), surface.get_pixel(x, y))
            else:
                continue
            break
    
    def get_dimensions(self):
        return (self.width, self.height)

    def reset(self):
        self.abort = True
