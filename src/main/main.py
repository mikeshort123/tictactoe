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

    d = 5
    s = 1

    corners, sides = generate_objects(s, d)

    r=0

    cam_pos = np.zeros((d,1))
    cam_pos[2,0] = -s*2-1


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        rotation = gen_rotator(r, d, 1, 2) @ gen_rotator(r, d, 0, 3)

        r += 0.01

        pygame.draw.rect(display, (0,0,0), (0, 0, WIDTH, HEIGHT))

        transformed = (rotation @ corners - cam_pos)
        points_xy = transformed[:2, :]
        points_z = np.sum(transformed[2:, :], axis=0)

        scaled = points_xy / points_z

        screen_pos = (ZOOM * scaled + np.array([[WIDTH], [HEIGHT]]) / 2).T


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
            edges.append((i, end_index))

    point_array = np.array(points).T - squares/2

    return point_array, edges

def gen_rotator(r, d, a, b):
    m = np.identity(d)

    m[a, a] = math.cos(r)
    m[a, b] =-math.sin(r)
    m[b, a] = math.sin(r)
    m[b, b] = math.cos(r)

    return m

if __name__ == '__main__': main()
