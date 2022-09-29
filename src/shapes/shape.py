import pygame
import numpy as np

class Shape:

    def __init__(self, indices, cubes):
        self.indices = np.array(indices)

        self.cubes = []
        for cube in cubes:
            if cube.owns(self.indices):
                self.cubes.append(cube)

    def get_dist(self, points):

        return np.sum(np.mean(points[:, self.indices], axis=1)**2)

    def is_active(self):
        if len(self.indices) == 2:
            return True
        else:
            for cube in self.cubes:
                if cube.active:
                    return True

        return False

    def render(self, points, display):

        corners = points[self.indices, :]

        if len(self.indices) == 2:
            pygame.draw.line(display, (0, 255, 255), corners[0], corners[1], width = 3)

        else:
            for cube in self.cubes:
                if cube.active:
                    pygame.draw.polygon(display, cube.colour, corners)
