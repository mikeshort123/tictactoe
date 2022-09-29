import pygame
import sys
import numpy as np
import math

def main():

    pygame.init()

    WIDTH, HEIGHT = 640, 480

    display = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    corners = np.array([
        [ 1, 1, 1],
        [ 1, 1,-1],
        [ 1,-1, 1],
        [ 1,-1,-1],
        [-1, 1, 1],
        [-1, 1,-1],
        [-1,-1, 1],
        [-1,-1,-1]
    ])

    sides = np.array([
        [0,1],
        [0,2],
        [0,4],
        [1,3],
        [1,5],
        [2,3],
        [2,6],
        [3,7],
        [4,5],
        [4,6],
        [5,7],
        [6,7]
    ])

    r=0

    cam_pos = np.array([0, 0, -6])


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        rotation = np.array([
            [math.cos(r), 0,-math.sin(r)],
            [0, 1, 0],
            [math.sin(r), 0, math.cos(r)]

        ])

        r += 0.01

        pygame.draw.rect(display, (0,0,0), (0, 0, WIDTH, HEIGHT))

        transformed = (corners @ rotation - cam_pos)
        points_xy = transformed[:, 0:2]
        points_z = transformed[:, 2:3]

        screen_pos = WIDTH * (points_xy / points_z) + np.array([WIDTH, HEIGHT]) / 2


        for point in screen_pos:

            pygame.draw.circle(display, (255,255,0), point, 5)

        for side in sides:
            pygame.draw.line(display, (0, 255, 255), screen_pos[side[0]], screen_pos[side[1]])


        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__': main()
