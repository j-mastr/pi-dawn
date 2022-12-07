import attr

@attr.s
class Color:
    r = attr.ib(type=int)
    g = attr.ib(type=int)
    b = attr.ib(type=int)

    def __iter__(self):
        yield self.r
        yield self.g
        yield self.b

    def __getitem__(self, key):
        return [*self][key]

    def interpolate(self, other: 'Color', factor: float):
        factor_inverse = 1 - factor
        interpolated = [round(color * factor + other[index] * factor_inverse) for index, color in enumerate(self)]

        return Color(*interpolated)


@attr.s
class GradientStop:
    pos = attr.ib(type=float)
    color = attr.ib(type=Color)


@attr.s(init=False)
class Surface:
    def __init__(self, screen):
        self.width = screen.width
        self.height = screen.height
        self.data = self.width * self.height * [Color(0, 0, 0)]

    def get_pixel(self, x, y):
        offset = y * self.width + x

        return self.data[offset]
    
    def set_pixel(self, pixel, color: Color):
        x, y = pixel
        offset = y * self.width + x
        self.data[offset] = color

        return self

    def draw(self, drawing):
        drawing.draw(self)

        return self

    def interpolate(self, other, factor):
        factor_inverse = 1 - factor
        for i in range(len(self.data)):
            self.data[i] = round(self.data[i] * factor + other.data[i] * factor_inverse)


class Geometry:
    def draw(self, surface):
        pass

class Gradient(Geometry):
    def __init__(self, stops):
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
            GradientStop(0.0, Color(0, 0, 0)),
            GradientStop(1.0, Color(0, 0, 0)),

        ])),
        SunriseAlarmStep(time=-0.67, gradient=Gradient([
            GradientStop(0.0, Color(51, 0, 105)),
            GradientStop(0.75, Color(51, 0, 105)),
            GradientStop(1.0, Color(255, 0, 0)),
        ])),
        SunriseAlarmStep(time=-0.33, gradient=Gradient([
            GradientStop(0.0, Color(127, 0, 0)),
            GradientStop(0.5, Color(127, 0, 0)),
            GradientStop(1.0, Color(255, 255, 0)),
        ])),
        SunriseAlarmStep(time=0, gradient=Gradient([
            GradientStop(0.0, Color(255, 255, 255)),
            GradientStop(1.0, Color(255, 255, 255)),
        ])),
        SunriseAlarmStep(time=1, gradient=Gradient([
            GradientStop(0.0, Color(255, 255, 255)),
            GradientStop(1.0, Color(255, 255, 255)),
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
        surface.interpolate(upper_key_frame.surface, 1-time_between_key_frames)
