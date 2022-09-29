import random
import numpy as np

class Hyper_Cube:

    def __init__(self, indices):

        self.indices = indices
        self.active = random.choice([True, False, False, False])
        self.colour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    def owns(self, indices):

        for p in indices:
            if p not in self.indices:
                return False

        return True

    @staticmethod
    def build_cube_list(squares, dimensions):
        points = squares+1
        cubes = []
        base = np.array([i for i in Hyper_Cube.base_generator(0, [points**i for i in range(dimensions)])])

        for offset in Hyper_Cube.offset_generator(0, 0, dimensions, points):
            cubes.append(Hyper_Cube(base + offset))

        return cubes

    @staticmethod
    def base_generator(t,l):

        if t == []:
            return

        yield t

        for i in range(len(l)):
            yield from Hyper_Cube.base_generator(t+l[i], l[i+1:])


    @staticmethod
    def offset_generator(total, depth, max_depth, points):

        if depth == max_depth:
            yield total
            return

        for i in range(points-1):
            yield from Hyper_Cube.offset_generator(i * points**depth + total, depth+1, max_depth, points)
