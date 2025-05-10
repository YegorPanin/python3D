import pygame
import numpy as np
from raycasting import Ray

class camera:
    def __init__(self, screen, width, height, position=(0, 0, -5), zoom=1.0):
        self.position = np.array(position, dtype=float)  # 3D позиция камеры
        self.screen = screen
        self.zoom = zoom
        self.width = width
        self.height = height

    def project(self, point_3d):
        """Проекция одной точки из 3D в 2D"""
        half_w = self.width / 2
        half_h = self.height / 2

        x, y, z = point_3d
        screen_x = int((x - self.position[0]) * self.zoom + half_w)
        screen_y = int((-y - self.position[1]) * self.zoom + half_h)
        return (screen_x, screen_y)

    def project_all(self, vertices):
        return [self.project(v) for v in vertices]

    def get_ray(self, local_pos, shape):
        """Создаёт луч из камеры через точку экрана (мыши)"""
        half_w = self.width / 2
        half_h = self.height / 2

        x = (local_pos[0] - half_w) / self.zoom + self.position[0]
        y = -(local_pos[1] - half_h) / self.zoom + self.position[1]
        z = self.position[2]

        origin = np.array([x, y, z])
        direction = np.array([0, 0, 1])  # Предположим, что камера смотрит по оси Z

        ray = Ray(origin, direction)
        closest_face = ray.cast(shape)
        color = (0,0,0)
        if closest_face:
            color = shape.color
        return color

    def draw(self, shape):
        for i in range(self.width):
            for j in range(self.height):
                pos = (i, j)
                color = self.get_ray(pos, shape)
                self.screen.set_at(pos, color)



