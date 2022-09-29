import pygame
import sys
import numpy as np
import math

from src.shapes.hyper_cube import Hyper_Cube
from src.shapes.shape import Shape

def main():

    pygame.init()

    WIDTH, HEIGHT = 640, 480
    ZOOM = 400

    display = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    d = 3
    s = 3

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

        ordered_shapes = sorted(shapes, reverse = True, key = lambda s : s.get_dist(transformed))
        filtered_shapes = filter(lambda s : s.is_active(), ordered_shapes)

        for shape in filtered_shapes:
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







if __name__ == '__main__': main()
