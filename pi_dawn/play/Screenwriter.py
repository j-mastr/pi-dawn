from .Play import BasePlay, Play, Act, StageDesign
from .WithDuration import PlayWithDuration
from pi_dawn.graphics import Geometry, Transition

class Screenwriter:
    def __init__(self, previous = None):
        self.previous = previous
        self.scene = None
        self.next = None

        if previous is not None:
            previous.next = self

    def write(self):
        if self.previous is None:
            play = Play()
        else:
            play = self.previous.write()

        act = self.get_act()
        if act is not None:
            play.append(act)

        return play

    def get_act(self):
        if isinstance(self.scene, BasePlay):
            return self.scene
        if isinstance(self.scene, Geometry.Geometry):
            return StageDesign(self.scene)
        if isinstance(self.scene, Transition.Transition):
            return Act(self.scene)
        if isinstance(self.scene, Screenwriter):
            return self.scene.write()
        return None

    def start_from(self, *args, act=StageDesign, **kwargs):
        return self.then(*args, act=act, **kwargs)

    def to(self, *args, act=StageDesign, **kwargs):
        return self.then(*args, act=act, **kwargs)

    def transition(self, *args, act=Act, **kwargs):
        return self.then(*args, act=act, **kwargs)

    def frame(self, *args, act=StageDesign, **kwargs):
        return self.then(*args, act=act, **kwargs)

    def duration(self, duration):
        return self.wrap(PlayWithDuration, duration)
    
    def replace(self, *args, act = Act, insert = False, replace = False, **kwargs):
        if len(args) == 0:
            return self
        
        self.scene = act(args[0], **kwargs)

        return self.then(*args[1:], act = Act, insert=insert, replace=replace, **kwargs)

    def then(self, *args, act = Act, insert = True, replace = True, **kwargs):
        if len(args) == 0:
            return self
        
        return self.chain(insert=insert, replace=replace).replace(*args, act=act, insert=insert, replace=replace, **kwargs)

    def wrap(self, wrapper, *args, **kwargs):
        if self.previous is None:
            self.insert_next(instance=WrappingScreenwriter).wrap(wrapper, *args, **kwargs)
        else:
            self.previous.wrap(wrapper, *args, **kwargs)

        return self

    def insert_next(self, instance=None):
        if instance is None:
            instance = Screenwriter
        if self.next is None:
            return self.get_next(instance)

        currentNext = self.next
        self.next = instance(previous = self)
        self.next.next = currentNext
        currentNext.previous = self.next

        return self.next

    def chain(self, insert = False, replace = False):
        if insert:
            return self.insert_next()
        elif replace:
            return Screenwriter(previous = self)
        else:
            return self.get_next()

    def get_next(self, instance=None):
        if instance is None:
            instance = Screenwriter
        if self.next is None:
            instance(previous = self)

        return self.next


class WrappingScreenwriter(Screenwriter):
    def __init__(self, previous = None):
        super().__init__(previous)
        self.wrapper = None

    def write(self):
        if self.previous is None:
            play = Play()
        else:
            play = self.previous.write()
        
        if self.wrapper is not None:
            wrapper, args, kwargs = self.wrapper

            return wrapper(play, *args, **kwargs)

        return play

    def replace(self, *args, act = Act, insert = False, replace = False, **kwargs):
        if len(args) == 0:
            return self
        # Do not replace current scene.
        # Propagate to next Screenwriter right away instead.
        return self.then(*args, act = Act, insert=insert, replace=replace, **kwargs)

    def wrap(self, wrapper, *args, **kwargs):
        if self.wrapper is None:
            self.wrapper = (wrapper, args, kwargs)
        else:
            self.insert_next(instance=WrappingScreenwriter).wrap(wrapper, *args, **kwargs)

        return self
