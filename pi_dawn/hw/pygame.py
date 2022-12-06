import attr
import pygame

from pi_dawn import graphics
from pi_dawn.hw.Hardware import Hardware

@attr.s(init=False)
class LedScreen(Hardware):
    width = attr.ib(type=int)
    height = attr.ib(type=int)

    def __init__(self, width, height, gamma_r=1, gamma_g=1, gamma_b=1):
        self.width = width
        self.height = height
        self.state = StateIdle(self)

        pygame.init()
        pygame.display.set_mode((10*self.width, 10*self.height))
        print("{}x{} (in theory)".format(self.width, self.height))

    def start_refresh(self):
        self.state.start_refresh()

    def refresh(self):
        self.state.refresh()

    def set_pixel(self, pixel, color):
        self.state.set_pixel(pixel, color)
    
    def set_state(self, state):
        self.state = state

class StateIdle:
    def __init__(self, screen):
        self.screen = screen
    
    def start_refresh(self):
        self.screen.set_state(StateRefresh(self.screen))
    
    def refresh(self):
        raise("Not in refresh state!")
    
    def set_pixel(self):
        raise("Not in refresh state!")

class StateRefresh:
    def __init__(self, screen):
        self.screen = screen

        self.pysurf = pygame.Surface((self.screen.width, self.screen.height), depth=32)
        self.pysurf.lock()
    
    def start_refresh(self):
        raise("Already refreshing!")
    
    def refresh(self):
        self.pysurf.unlock()

        bg = pygame.display.get_surface()
        pygame.transform.scale(self.pysurf, (bg.get_width(), bg.get_height()), bg)
        pygame.display.flip()

        self.screen.set_state(StateIdle(self.screen))
    
    def set_pixel(self, pixel, color):
        self.pysurf.set_at(pixel, color)
