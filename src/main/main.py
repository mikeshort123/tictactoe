import pygame
import sys
import numpy as np
import math
import random

def main():

    pygame.init()

    WIDTH, HEIGHT = 640, 480
    ZOOM = 400

    display = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    d = 3
    s = 2

    shapes = []

    corners, shapes, cubes = generate_objects(s, d)



    r=0

    cam_pos = np.zeros((d,1)) - s - 1
    cam_pos[0,0] = 0
    cam_pos[1,0] = 0



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        rotation = gen_rotator(r, d, 1, 2) @ gen_rotator(r, d, 0, 2)

        r += 0.01

        pygame.draw.rect(display, (0,0,0), (0, 0, WIDTH, HEIGHT))

        transformed = (rotation @ corners - cam_pos)
        points_xy = transformed[:2, :]
        points_z = np.sum(transformed[2:, :], axis=0)

        scaled = points_xy / points_z

        screen_pos = (ZOOM * scaled + np.array([[WIDTH], [HEIGHT]]) / 2).T


        #for point in screen_pos:
            #pygame.draw.circle(display, (255,255,0), point, 5)

        ordered_shapes = sorted(shapes, reverse = True, key = lambda s : s.get_dist(transformed))

        for shape in ordered_shapes:
            shape.render(screen_pos, display)


        pygame.display.update()
        clock.tick(60)

def point_generator(n, b, d):

    l = []
    for i in range(d):

        l.append((n//(b**i))%b)

    return l

def point_index(l, b, d):
    t = 0
    for i, p in enumerate(l):
        t += p * (b ** i)

    return t


def generate_objects(squares, dimensions):

    points = []
    edges = []
    faces = []

    cubes = Hyper_Cube.build_cube_list(squares, dimensions)

    n_points = squares+1


    for p1_index in range(n_points**dimensions):
        p1 = point_generator(p1_index, n_points, dimensions)

        points.append(p1)

        for index_a in range(dimensions):

            if p1[index_a] >= squares:
                    continue

            end = p1[:]
            end[index_a] += 1
            end_index = point_index(end, n_points, dimensions)
            edges.append((p1_index, end_index))

            for index_b in range(dimensions):

                if index_a >= index_b:
                    continue

                if p1[index_b] >= squares:
                    continue


                p2 = p1[:]
                p2[index_a] += 1
                p2_index = point_index(p2, n_points, dimensions)

                p3 = p1[:]
                p3[index_b] += 1
                p3_index = point_index(p3, n_points, dimensions)

                p4 = p1[:]
                p4[index_a] += 1
                p4[index_b] += 1
                p4_index = point_index(p4, n_points, dimensions)

                faces.append((p1_index, p2_index, p4_index, p3_index))

    point_array = np.array(points).T - squares/2

    shapes = []
    for edge in edges:
        shapes.append(Shape(edge, cubes))
    for face in faces:
        shapes.append(Shape(face, cubes))

    return point_array, shapes, cubes

def gen_rotator(r, d, a, b):
    m = np.identity(d)

    m[a, a] = math.cos(r)
    m[a, b] =-math.sin(r)
    m[b, a] = math.sin(r)
    m[b, b] = math.cos(r)

    return m

class Shape:

    def __init__(self, indices, cubes):
        self.indices = np.array(indices)

        self.cubes = []
        for cube in cubes:
            if cube.owns(self.indices):
                self.cubes.append(cube)

    def get_dist(self, points):

        return np.sum(np.mean(points[:, self.indices], axis=1)**2)

    def render(self, points, display):

        corners = points[self.indices, :]

        if len(self.indices) == 2:
            pygame.draw.line(display, (0, 255, 255), corners[0], corners[1], width = 5)

        else:
            for cube in self.cubes:
                if cube.active == True:
                    pygame.draw.polygon(display, cube.colour, corners)
                    return


class Hyper_Cube:

    def __init__(self, indices):

        self.indices = indices
        self.active = random.choice([True, False])
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


if __name__ == '__main__': main()
