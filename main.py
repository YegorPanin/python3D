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
cam = camera(screen)

# Вершины внешнего куба (исходный куб)
cube_verts = [
    (-50, -50, -50), (50, -50, -50), (50, 50, -50), (-50, 50, -50),
    (-50, -50, 50), (50, -50, 50), (50, 50, 50), (-50, 50, 50)
]

# Вершины внутреннего куба (уменьшенный в 2 раза)
inner_cube_verts = [(x/2, y/2, z/2) for x, y, z in cube_verts]

# Общий список вершин гиперкуба
hypercube_verts = cube_verts + inner_cube_verts

# Рёбра внешнего куба (из оригинального куба)
tetra_verts = [
    (0, 0, 0),  # A
    (1, 0, 0),  # B
    (0.5, math.sqrt(3)/2, 0),  # C
    (0.5, math.sqrt(3)/6, math.sqrt(6)/3)  # D (вершина пирамиды)
]

# Рёбра тетраэдра (соединяют все пары вершин)
tetra_edges = [
    (0, 1), (0, 2), (0, 3),  # Рёбра от основания к вершине
    (1, 2), (1, 3),          # Рёбра основания и боковые
    (2, 3)                   # Последнее боковое ребро
]
cube = shape3D(tetra_verts, tetra_edges, color=(0, 255, 0))

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pygame.quit()
            sys.exit()
    cube.rotate(0.001, 0.001)
    screen.fill(BACKGROUND_COLOR)

    cam.draw(cube,screen)

    Controller.listen_control(cube)
    pg.display.update()
    clock.tick(FPS)
