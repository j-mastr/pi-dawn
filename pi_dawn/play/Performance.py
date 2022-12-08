import attr
import functools


@attr.s
class KeyFrame:
    time = attr.ib()
    duration = 0
    surface = attr.ib()


@attr.s
class Actor:
    time = attr.ib()
    duration = attr.ib()
    transition = attr.ib()


class Performance:
    def __init__(self, scenes):
        self.key_frames = [s for s in scenes if isinstance(s, KeyFrame)]
        self.actors = [s for s in scenes if isinstance(s, Actor)]

    def scene(self, time):
        active_actor = None
        lower_key_frame = None
        upper_key_frame = None
        for key_frame in self.key_frames:
            if time >= key_frame.time and (lower_key_frame is None or key_frame.time > lower_key_frame.time):
                lower_key_frame = key_frame
            if time < key_frame.time and (upper_key_frame is None or key_frame.time < upper_key_frame.time):
                upper_key_frame = key_frame

        for actor in self.actors:
            if time >= actor.time and time < actor.time + actor.duration:
                active_actor = actor

        return Scene(active_actor.transition if active_actor else None, lower_key_frame, upper_key_frame, (time-active_actor.time)/active_actor.duration if active_actor else time)

    def get_duration(self):
        return self.key_frames[-1].duration

    def __str__(self):
        return "{}({})".format(__class__, self.key_frames)


class Scene:
    def __init__(self, actor, lower_key_frame, upper_key_frame, time):
        self.actor = actor
        self.lower_key_frame = lower_key_frame
        self.upper_key_frame = upper_key_frame
        self.time = time

    def draw(self, surface):
        if self.lower_key_frame:
            surface.data = self.lower_key_frame.surface.data[:]
        if self.actor:
            surface.draw(self.actor.step(self.time, self.upper_key_frame.surface))