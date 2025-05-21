import pygame
import numpy as np
from raycasting import Ray

class camera:
    def __init__(self, screen, width, height, position=(0, 0, -150), zoom=500):
        self.position = np.array(position, dtype=float)  # Позиция камеры в 3D (x, y, z)
        self.screen = screen
        self.zoom = zoom
        self.width = width
        self.height = height
        self.yaw = 0.0  # Поворот вокруг оси Y (влево/вправо)
        self.pitch = 0.0  # Поворот вокруг оси X (вверх/вниз)

    def move(self, dx, dy, dz):
        self.position += np.array([dx,dy,dz])

    def project(self, point_3d):
        """Проекция точки из 3D в 2D с учетом поворотов и перспективы"""
        # Шаг 1: Перенос точки относительно камеры
        trans_point = point_3d - self.position
        x, y, z = trans_point

        # Шаг 2: Поворот вокруг оси Y (yaw)
        cos_yaw, sin_yaw = np.cos(self.yaw), np.sin(self.yaw)
        x_rot = x * cos_yaw + z * sin_yaw
        z_rot = -x * sin_yaw + z * cos_yaw

        # Шаг 3: Поворот вокруг оси X (pitch)
        cos_pitch, sin_pitch = np.cos(self.pitch), np.sin(self.pitch)
        y_rot = y * cos_pitch - z_rot * sin_pitch
        z_rot_new = y * sin_pitch + z_rot * cos_pitch

        # Проверка, не находится ли точка за камерой
        if z_rot_new <= 0:
            return None  # Точка за камерой — не рисуем

        # Шаг 4: Перспективная проекция
        scale = self.zoom / z_rot_new
        screen_x = int(x_rot * scale + self.width / 2)
        screen_y = int(-y_rot * scale + self.height / 2)  # Инвертируем Y

        return (screen_x, screen_y)

    def project_all(self, vertices):
        """Проекция всех вершин с учетом проверки на видимость"""
        projected = []
        for v in vertices:
            proj = self.project(v)
            projected.append(proj)
        return projected

    def draw(self, shape):
        pos = self.position
        vertices = shape.vertices
        projected_verts = self.project_all(vertices)

        for face in shape.faces:
            # Получаем индексы вершин для грани
            i0, i1, i2 = face
            v0 = projected_verts[i0]
            v1 = projected_verts[i1]
            v2 = projected_verts[i2]

            # Пропускаем грань, если хотя бы одна вершина вне видимости
            if None in (v0, v1, v2):
                continue

            # Центр грани для расчета расстояния
            center = np.mean([vertices[i0], vertices[i1], vertices[i2]], axis=0)
            distance = int(np.linalg.norm(center - pos))

            # Рассчитываем цвет с учетом расстояния
            color = shape.color
            color = (
                max(0, color[0] - 0.5 * distance),
                max(0, color[1] - distance),
                max(0, color[2] - distance)
            )

            # Рисуем грань
            pygame.draw.polygon(self.screen, color, [v0, v1, v2])