import pygame
import numpy as np
from raycasting import Ray

class Camera:
    def __init__(self, screen, width, height, position=(0, 0, -150), zoom=500):
        self.position = np.array(position, dtype=float)
        self.screen = screen
        self.zoom = zoom
        self.width = width
        self.height = height
        self.yaw = 0.0
        self.pitch = 0.0
        self.shapes = []  # Хранение объектов Shape3D

    def move(self, dx, dy, dz):
        """Перемещение камеры по осям"""
        self.position += np.array([dx, dy, dz])

    def rotate(self, dyaw, dpitch):
        """Поворот камеры (изменение yaw и pitch)"""
        self.yaw += dyaw
        self.pitch += dpitch
        self.pitch = np.clip(self.pitch, -np.pi / 2, np.pi / 2)

    def project(self, point_3d):
        """Проекция точки из 3D в 2D с учетом поворотов и перспективы"""
        trans_point = point_3d - self.position
        x, y, z = trans_point

        # Поворот вокруг Y (yaw)
        cos_yaw, sin_yaw = np.cos(self.yaw), np.sin(self.yaw)
        x_rot = x * cos_yaw + z * sin_yaw
        z_rot = -x * sin_yaw + z * cos_yaw

        # Поворот вокруг X (pitch)
        cos_pitch, sin_pitch = np.cos(self.pitch), np.sin(self.pitch)
        y_rot = y * cos_pitch - z_rot * sin_pitch
        z_rot_new = y * sin_pitch + z_rot * cos_pitch

        if z_rot_new <= 0:
            return None

        # Перспективная проекция
        scale = self.zoom / z_rot_new
        screen_x = int(x_rot * scale + self.width / 2)
        screen_y = int(-y_rot * scale + self.height / 2)

        return (screen_x, screen_y)

    def add(self, shape):
        """Добавление объекта Shape3D"""
        self.shapes.append(shape)

    def draw(self):
        """Отрисовка всех объектов в порядке удалённости"""
        all_polygons = []

        for shape in self.shapes:
            vertices = shape.vertices
            projected_verts = [self.project(v) for v in vertices]

            for face in shape.faces:
                indices = list(face)
                points = [projected_verts[i] for i in indices]
                if None in points:
                    continue

                # Центр грани
                face_vertices = [vertices[i] for i in indices]
                center = np.mean(face_vertices, axis=0)
                distance = np.linalg.norm(center - self.position)

                # Цвет с учетом расстояния
                color = shape.color
                color = (
                    max(0, int(color[0] - 0.5 * distance)),
                    max(0, int(color[1] - distance)),
                    max(0, int(color[2] - distance))
                )

                all_polygons.append({
                    'distance': distance,
                    'points': points,
                    'color': color
                })

        # Сортировка по расстоянию (от дальнего к ближнему)
        all_polygons.sort(key=lambda p: p['distance'], reverse=True)

        # Отрисовка
        for poly in all_polygons:
            pygame.draw.polygon(self.screen, poly['color'], poly['points'])