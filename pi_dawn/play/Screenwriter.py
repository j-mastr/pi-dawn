from .Play import BasePlay, Play, Act, StageDesign
from .WithDuration import PlayWithDuration
from pi_dawn.graphics import Geometry, Transition

class Screenwriter:
    def __init__(self, speed = None, previous = None):
        self.previous = previous
        self.speed = speed
        self.scene = None
        self.next = None

        if previous is not None:
            previous.next = self

    def write(self):
        if self.previous is None:
            play = Play()
            if self.speed is not None:
                play = PlayWithDuration(play, self.speed)
            return play
        
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

    def duration(self, speed):
        if self.previous is None:
            self.speed = speed
        else:
            self.previous.duration(speed)

        return self
    
    def replace(self, *args, act = Act, insert = False, replace = False, **kwargs):
        if len(args) == 0:
            return self
        
        self.scene = act(args[0], **kwargs)

        return self.then(*args[1:], act = Act, insert=insert, replace=replace, **kwargs)

    def then(self, *args, act = Act, insert = True, replace = True, **kwargs):
        if len(args) == 0:
            return self
        
        return self.chain(insert=insert, replace=replace).replace(*args, act=act, insert=insert, replace=replace, **kwargs)
    
    def insert_next(self):
        if self.next is None:
            return self.get_next()

        currentNext = self.next
        self.next = Screenwriter(previous = self)
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

    def get_next(self):
        if self.next is None:
            Screenwriter(previous = self)

        return self.next
