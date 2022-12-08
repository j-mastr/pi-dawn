import attr

from rpi_ws281x import PixelStrip, Color as StripColor, ws

from pi_dawn import graphics
from pi_dawn.graphics import Color
from pi_dawn.hw.Hardware import Hardware


LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 30   # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP = ws.SK6812_STRIP_GRBW


@attr.s(init=False)
class WS281x(Hardware):
    length = attr.ib(type=int)

    def __init__(self, length):
        self.length = length

        self.pixels = PixelStrip(length, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
        self.pixels.begin()

    def set_pixel(self, screen, pixel, color: Color):
        offset, y = pixel
        self.pixels.setPixelColor(offset, StripColor(*color))
    
    def refresh(self):
        self.pixels.show()

    def get_dimensions(self):
        return (self.length, 1)
