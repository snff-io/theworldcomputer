import random

class Pair:
    def __init__(self, x, y, top_type, bottom_type, magnitude=1, pressure=0, layer=0):
        self.x = x
        self.y = y
        self.topType = top_type
        self.bottomType = bottom_type
        self.magnitude = magnitude
        self.pressure = pressure
        self.layer = layer

    
    stability_table = [
        [-1, 1, 2, 3, 4, 5, 6, 7, 8],
        [1, 1, 0, 0, 0, 0, 0, 0, 0],
        [2, 1, 1, 1, 0, 1, 1, 1, 1],
        [3, 1, 0, 1, 1, 1, 1, 0, 0],
        [4, 1, 0, 0, 1, 1, 1, 0, 0],
        [5, 1, 0, 0, 0, 1, 0, 0, 0],
        [6, 1, 0, 0, 0, 1, 1, 0, 0],
        [7, 1, 0, 0, 0, 1, 1, 1, 1],
        [8, 1, 0, 0, 1, 1, 1, 0, 1]
    ]

    # Functions
    @staticmethod
    def check_stability(top_type, bottom_type):
        return Pair.stability_table[bottom_type][top_type]

    @staticmethod
    def random_individual(x, y, layer=0):
        random.seed(144000)
        top_type = random.randint(1, 8)
        bottom_type = random.randint(1, 8)
        magnitude = 1
        pressure = 0
        return Pair(x, y, top_type, bottom_type, magnitude, pressure, layer)

    @property
    def max_magnitude(self):
        return 50

    @property
    def stability(self):
        return self.stability_table[self.bottomType][self.topType]

    def copy(self):
        return Pair(self.x, self.y, self.topType, self.bottomType, self.magnitude, self.pressure, self.layer)

    def __str__(self):
        return f"{self.stability}{self.topType}{self.bottomType};{self.magnitude:.2f};{self.pressure:.2f};{self.layer}:{self.x}:{self.y}"

__all__ = { Pair }