import pygame
import numpy as np

class camera:
    def __init__(self, screen, position=(0, 0, -5), zoom=1.0):
        self.position = np.array(position, dtype=float)  # 3D позиция камеры
        self.zoom = zoom

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

    def get_ray(self, mouse_pos):
        """Создаёт луч из камеры через точку экрана (мыши)"""
        half_w = self.width / 2
        half_h = self.height / 2

        x = (mouse_pos[0] - half_w) / self.zoom + self.position[0]
        y = -(mouse_pos[1] - half_h) / self.zoom + self.position[1]
        z = self.position[2]

        origin = np.array([x, y, z])
        direction = np.array([0, 0, 1])  # Предположим, что камера смотрит по оси Z

        return Ray(origin, direction)


# ==================== Raycasting ====================
class Ray:
    def __init__(self, origin, direction):
        self.origin = np.array(origin)
        self.direction = np.array(direction) / np.linalg.norm(direction)

    def intersect_triangle(self, A, B, C):
        """Проверяет пересечение луча с треугольником ABC"""
        # Нормаль к плоскости
        AB = np.array(B) - np.array(A)
        AC = np.array(C) - np.array(A)
        normal = np.cross(AB, AC)
        normal /= np.linalg.norm(normal)

        denom = np.dot(normal, self.direction)
        if abs(denom) < 1e-6:
            return None  # Луч параллелен плоскости

        t = np.dot(normal, np.array(A) - self.origin) / denom
        if t < 0:
            return None  # Пересечение за камерой

        P = self.origin + t * self.direction  # Точка пересечения

        # Проверяем, внутри ли треугольника
        def same_side(p1, p2, a, b):
            cp1 = np.cross(b - a, p1 - a)
            cp2 = np.cross(b - a, p2 - a)
            return np.dot(cp1, cp2) >= 0

        if same_side(P, B, A, C) and same_side(P, C, B, A) and same_side(P, A, C, B):
            return t, P
        else:
            return None

    def cast(self, shape):
        closest = None
        for face in shape.faces:
            if len(face) == 3:
                A, B, C = [shape.vertices[i] for i in face]
                result = self.intersect_triangle(A, B, C)
                if result and (closest is None or result[0] < closest[0]):
                    closest = result
        return closest
