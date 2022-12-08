import attr
import functools

from .Performance import Actor, KeyFrame, Performance


class BasePlay:
    def act(self, led_screen):
        scenes = self.generate(led_screen)
        return Performance(scenes)

    def get_duration(self):
        return 0

    def generate(self, led_screen):
        return []

    def __str__(self):
        return "{}([{}])".format(__class__, self.acts)


class Play(BasePlay):
    def __init__(self, acts = []):
        self.acts = acts

    def get_duration(self):
        return functools.reduce(lambda duration, act: duration+act.get_duration(), self.acts, 0)

    def generate(self, led_screen):
        scenes = []
        timeOffset = 0
        for act in self.acts:
            generated = act.generate(led_screen)
            for g in generated:
                g.time = timeOffset + g.time
                if hasattr(g, "duration"):
                    timeOffset = g.time + g.duration
            scenes = scenes + generated

        return scenes

    def append(self, act):
        self.acts.append(act)


class Act(BasePlay):
    def __init__(self, show, duration):
        self.show = show
        self.duration = duration

    def get_duration(self):
        return self.duration

    def generate(self, led_screen):
        return [Actor(transition=self.show, time=0, duration=self.get_duration())]

    def __str__(self):
        return "{}({})".format(__class__, self.show)


class StageDesign(Act):
    def __init__(self, show):
        super().__init__(show, 0)

    def get_duration(self):
        return 0

    def generate(self, led_screen):
        surface = led_screen.make_surface()
        surface.draw(self.show)
        return [KeyFrame(surface=surface, time=0)]
