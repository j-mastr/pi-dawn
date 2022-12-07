import attr
from typing import List

from .Color import Color


class Geometry:
    def draw(self, surface):
        pass


class Gradient(Geometry):
    @attr.s
    class Stop:
        pos = attr.ib(type=float)
        color = attr.ib(type=Color)

    def __init__(self, stops: List[Stop]):
        self.stops = stops

    def draw(self, surface):
        for y in range(surface.height):
            pos = y / surface.height
            lower_stop = self.stops[0]
            upper_stop = self.stops[-1]
            for stop in self.stops:
                if pos >= stop.pos and stop.pos > lower_stop.pos:
                    lower_stop = stop
                if pos < stop.pos and stop.pos < upper_stop.pos:
                    upper_stop = stop

            pos_diff = upper_stop.pos - lower_stop.pos
            pos_between_stops = (pos - lower_stop.pos) / pos_diff
            pos_between_stops_inverse = 1 - pos_between_stops

            color = upper_stop.color.interpolate(lower_stop.color, pos_between_stops)
            surface.draw(HorizontalLine(y, color))


class Rectangle(Geometry):
    def __init__(self, start, end, color: Color):
        self.start = start
        self.end = end
        self.color = color
    
    def draw(self, surface):
        startX, startY = self.start
        endX, endY = self.end

        minX = min(startX, endX)
        maxX = max(startX, endX)
        minY = min(startY, endY)
        maxY = max(startY, endY)

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                # TODO Fill using array methods?
                surface.set_pixel((x, y), self.color)


class Line(Geometry):
    def __init__(self, start, end, color: Color):
        self.start = start if start[0] <= end[0] else end
        self.end = end if start[0] <= end[0] else start
        self.color = color
    
    def draw(self, surface):
        diff = (self.end[0] - self.start[0], self.end[1] - self.start[1])
        gradient = diff[1] / diff[0]
        offset = self.start[1] - gradient * self.start[0]

        if abs(gradient) <= 1:
            for x in range(self.start[0], self.end[0] + 1):
                y = round(gradient * x + offset)
                surface.set_pixel((x, y), self.color)
        else:
            for y in range(self.start[1], self.end[1] + 1):
                x = round((y - offset) / gradient)
                surface.set_pixel((x, y), self.color)


class HorizontalLine(Line):
    def __init__(self, y, color: Color):
        super().__init__((0, y), (1, y), color)
    
    def draw(self, surface):
        self.end = (surface.width - 1, self.end[1])
        super().draw(surface)


class Fill(Geometry):
    def __init__(self, color: Color):
        self.color = color

    def draw(self, surface):
        surface.data = surface.width * surface.height * [self.color]
