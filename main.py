import pygame
import pygame as pg
import numpy as np
from camera import camera
import sys
from controller import Controller
from shapes import shape3D
import math

HEIGHT = 600
WIDTH = 800
BACKGROUND_COLOR = (0,0,0)
screen = pg.display.set_mode((WIDTH,HEIGHT))
FPS = 60
clock = pg.time.Clock()
cam = camera(screen, WIDTH, HEIGHT)
n = 10

vertices = [
        (-n, -n, -n), (n, -n, -n), (n, n, -n), (-n, n, -n),
        (-n, -n, n), (n, -n, n), (n, n, n), (-n, n, n)
    ]
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]
faces = [
    (0,1,2),
    (0,2,3),
    (0,3,7),
    (0,4,7),
    (0,1,4),
    (1,4,5),
    (5,1,6),
    (2,1,6),
    (3,7,2),
    (2,7,6),
    (4,5,6),
    (4,7,6)
]

cube = shape3D(vertices, edges, faces, color=(255, 0, 0))

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pygame.quit()
            sys.exit()
    cube.rotate(0.001, 0.001)
    screen.fill(BACKGROUND_COLOR)

    cam.draw(cube)

    Controller.listen_control(cube)
    pg.display.update()
    clock.tick(FPS)
