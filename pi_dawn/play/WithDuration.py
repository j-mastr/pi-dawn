from .Play import BasePlay
from .Performance import Performance


class PlayWithDuration(BasePlay):
    def __init__(self, play, duration):
        self.play = play
        self.duration = duration

    def get_duration(self):
        return self.duration

    def act(self, led_screen):
        return PerformanceWithDuration(super().act(led_screen), self.get_duration())

    def generate(self, led_screen):
        scenes = self.play.generate(led_screen)
        factor =  1 / self.play.get_duration()
        for scene in scenes:
            scene.time = factor * scene.time
            if hasattr(scene, "duration"):
                scene.duration = factor * scene.duration

        return scenes

    def append(self, act):
        self.play.append(act)


class PerformanceWithDuration(Performance):
    def __init__(self, performance, duration):
        self.performance = performance
        self.duration = duration

    def scene(self, time):
        return self.performance.scene(time/self.duration)

    def __str__(self):
        return "{}({})".format(__class__, self.performance.key_frames)