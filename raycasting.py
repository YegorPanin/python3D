import numpy as np
class Ray:
    def __init__(self, origin, direction):
        self.origin = np.array(origin)
        self.direction = np.array(direction) / np.linalg.norm(direction)

    def intersect_triangle(self, A, B, C):
        """Проверяет пересечение луча с треугольником ABC"""
        # Нормаль к плоскости
        A = np.array(A)
        B = np.array(B)
        C = np.array(C)
        AB = B-A
        AC = B-C
        normal = np.cross(AB, AC)
        normal /= np.linalg.norm(normal)

        denom = np.dot(normal, self.direction)
        if abs(denom) < 1e-6:
            return None  # Луч параллелен плоскости

        t = np.dot(normal, np.array(A) - self.origin) / denom
        if t < 0:
            return None  # Пересечение за камерой

        P = np.array(self.origin + t * self.direction)  # Точка пересечения

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
