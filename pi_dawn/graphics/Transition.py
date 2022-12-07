import attr


class Transition:
    def __init__(self, duration):
        self.duration = duration
    def step(self, *args, **kwargs):
        return self.Step(self, *args, **kwargs)

    class Step:
        def __init__(self, transition):
            self.transition = transition
        def draw(self, surface):
            pass


class Blend(Transition):
    class Step(Transition.Step):
        def __init__(self, transition, pos, nextFrame):
            super().__init__(transition)
            self.pos = pos
            self.nextFrame = nextFrame

        def draw(self, surface):
            factor = self.pos / self.transition.duration
            factor_inverse = 1 - factor
            for i in range(len(surface.data)):
                surface.data[i] = surface.data[i].interpolate(self.nextFrame.data[i], factor)
