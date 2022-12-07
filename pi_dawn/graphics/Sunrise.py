import attr

from .Color import Color
from .Geometry import Gradient
from .Surface import Surface
from .Transition import Blend

@attr.s
class SunriseAlarmStep:
    time = attr.ib()
    gradient = attr.ib()


@attr.s
class KeyFrame:
    time = attr.ib()
    surface = attr.ib()

@attr.s(init=False)
class Sunrise:

    steps = [
        SunriseAlarmStep(time=-1.0, gradient=Gradient([
            Gradient.Stop(0.0, Color(0, 0, 0)),
            Gradient.Stop(1.0, Color(0, 0, 0)),

        ])),
        SunriseAlarmStep(time=-0.67, gradient=Gradient([
            Gradient.Stop(0.0, Color(51, 0, 105)),
            Gradient.Stop(0.75, Color(51, 0, 105)),
            Gradient.Stop(1.0, Color(255, 0, 0)),
        ])),
        SunriseAlarmStep(time=-0.33, gradient=Gradient([
            Gradient.Stop(0.0, Color(127, 0, 0)),
            Gradient.Stop(0.5, Color(127, 0, 0)),
            Gradient.Stop(1.0, Color(255, 255, 0)),
        ])),
        SunriseAlarmStep(time=0, gradient=Gradient([
            Gradient.Stop(0.0, Color(255, 255, 255)),
            Gradient.Stop(1.0, Color(255, 255, 255)),
        ])),
        SunriseAlarmStep(time=1, gradient=Gradient([
            Gradient.Stop(0.0, Color(255, 255, 255)),
            Gradient.Stop(1.0, Color(255, 255, 255)),
        ])),
    ]

    def __init__(self, led_screen):
        self.key_frames = []

        for step in self.steps:
            surface = led_screen.make_surface()
            surface.draw(step.gradient)
            self.key_frames.append(KeyFrame(step.time, surface))

    def draw(self, surface: Surface, time: float):
        lower_key_frame = self.key_frames[0]
        upper_key_frame = self.key_frames[-1]
        for key_frame in self.key_frames:
            if time >= key_frame.time and key_frame.time > lower_key_frame.time:
                lower_key_frame = key_frame
            if time < key_frame.time and key_frame.time < upper_key_frame.time:
                upper_key_frame = key_frame
        time_between_key_frames = (time - lower_key_frame.time) / (upper_key_frame.time - lower_key_frame.time)
        surface.data = lower_key_frame.surface.data[:]
        surface.draw(Blend(1).step(1-time_between_key_frames, upper_key_frame.surface))
