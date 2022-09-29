import pygame
import sys
import numpy as np
import math

def main():

    pygame.init()

    WIDTH, HEIGHT = 640, 480
    ZOOM = 400

    display = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    d = 3

    corners, sides = generate_objects(1, d)

    r=0

    cam_pos = np.array([0, 0, -6])


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        rotation_a = np.array([
            [math.cos(r), 0,-math.sin(r)],
            [0, 1, 0],
            [math.sin(r), 0, math.cos(r)]

        ])

        rotation_b = np.array([
            [math.cos(r), -math.sin(r), 0],
            [math.sin(r),  math.cos(r), 0],
            [0, 0, 1]

        ])

        rotation = rotation_a @ rotation_b

        r += 0.01

        pygame.draw.rect(display, (0,0,0), (0, 0, WIDTH, HEIGHT))

        transformed = (corners @ rotation - cam_pos)
        points_xy = transformed[:, 0:2]
        points_z = transformed[:, 2:3]

        screen_pos = ZOOM * (points_xy / points_z) + np.array([WIDTH, HEIGHT]) / 2


        for point in screen_pos:

            pygame.draw.circle(display, (255,255,0), point, 5)

        for side in sides:
            pygame.draw.line(display, (0, 255, 255), screen_pos[side[0]], screen_pos[side[1]])


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

    n_points = squares+1



    for i in range(n_points**dimensions):
        n = point_generator(i, n_points, dimensions)

        points.append(n)

        for index, value in enumerate(n):

            if n[index] >= squares:
                continue

            end = n[:]
            end[index] += 1
            end_index = point_index(end, n_points, dimensions)
            edges.append([i, end_index])

    return np.array(points) - squares/2, np.array(edges)


if __name__ == '__main__': main()
