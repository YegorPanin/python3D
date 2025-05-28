import pygame
import pygame as pg
import numpy as np
from camera import Camera
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
cam = Camera(screen, WIDTH, HEIGHT)
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
floor_verts = []
floor_faces = []

# Параметры сетки
grid_size = 10  # 10x10 квадратов -> 100 квадратов, 200 треугольников
step = 20  # шаг между вершинами

# Генерация вершин
for x in range(grid_size + 1):
    for z in range(grid_size + 1):
        # координаты вершины
        vertex = (x * step - grid_size * step / 2, -50, z * step - grid_size * step / 2)
        floor_verts.append(vertex)

# Генерация полигонов (каждый квадрат делится на два треугольника)
index = 0
for x in range(grid_size):
    for z in range(grid_size):
        # Индексы вершин квадрата
        a = z * (grid_size + 1) + x
        b = a + 1
        c = a + (grid_size + 1)
        d = c + 1

        # Первый треугольник
        floor_faces.append((a, b, c))
        # Второй треугольник
        floor_faces.append((c, b, d))

floor = shape3D(floor_verts, [], floor_faces, color = (0,225,0))

cube = shape3D(vertices, edges, faces, color=(255, 0, 0))
cam.add(cube)
cam.add(floor)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pygame.quit()
            sys.exit()
    cube.rotate(0.001, 0.001)
    screen.fill(BACKGROUND_COLOR)

    cam.draw()

    Controller.listen_control(cam)
    pg.display.update()
    clock.tick(FPS)
