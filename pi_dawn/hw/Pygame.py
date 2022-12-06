import attr
import pygame

from pi_dawn import graphics
from pi_dawn.hw.Hardware import Hardware

@attr.s(init=False)
class Pygame(Hardware):
    width = attr.ib(type=int)
    height = attr.ib(type=int)

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.state = StateIdle(self)
        self.pysurf = pygame.Surface((self.width, self.height), depth=32)

        pygame.init()
        pygame.display.set_mode((10*self.width, 10*self.height))
        print("{}x{} (in theory)".format(self.width, self.height))

    def start_refresh(self):
        self.state.start_refresh()

    def refresh(self):
        self.state.refresh()

    def set_pixel(self, screen, pixel, color):
        self.state.set_pixel(screen, pixel, color)
    
    def set_state(self, state):
        self.state = state
    
    def get_dimensions(self):
        return (self.width, self.height)

class StateIdle:
    def __init__(self, screen):
        self.screen = screen
    
    def start_refresh(self):
        self.screen.set_state(StateRefresh(self.screen))
    
    def refresh(self):
        raise("Not in refresh state!")
    
    def set_pixel(self, screen, pixel, color):
        raise("Not in refresh state!")

class StateRefresh:
    def __init__(self, screen):
        self.screen = screen
        self.screen.pysurf.lock()
    
    def start_refresh(self):
        raise("Already refreshing!")
    
    def refresh(self):
        self.screen.pysurf.unlock()

        bg = pygame.display.get_surface()
        pygame.transform.scale(self.screen.pysurf, (bg.get_width(), bg.get_height()), bg)
        pygame.display.flip()

        self.screen.set_state(StateIdle(self.screen))
    
    def set_pixel(self, screen, pixel, color):
        self.screen.pysurf.set_at(pixel, color)
