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
        if factor > 1 or factor < 0:
            raise Exception("Factor out of range!")

        factor_inverse = 1 - factor
        interpolated = [round(color * factor + other[index] * factor_inverse) for index, color in enumerate(self)]

        return Color(*interpolated)
