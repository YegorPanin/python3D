from shapes import shape3D
import numpy as np


class grid(shape3D):
    def __init__(self, f, range_x, range_z, step=1):
        """
        Создает 3D-сетку на основе функции f(x, z)

        Параметры:
        f (callable): Функция f(x, z) -> y
        range_x (tuple): Диапазон по X (start, end)
        range_z (tuple): Диапазон по Z (start, end)
        step (float): Шаг сетки
        """
        # Генерация координатной сетки
        x_start, x_end = range_x
        z_start, z_end = range_z

        x_vals = np.arange(x_start, x_end + step, step)
        z_vals = np.arange(z_start, z_end + step, step)

        # Создание вершин
        vertices = []
        for z in z_vals:
            for x in x_vals:
                y = f(x, z)
                vertices.append((x, y, z))

        # Создание рёбер
        edges = []
        rows = len(z_vals)
        cols = len(x_vals)

        # Горизонтальные рёбра (по строкам)
        for row in range(rows):
            for col in range(cols - 1):
                current = row * cols + col
                next_vertex = current + 1
                edges.append((current, next_vertex))

        # Вертикальные рёбра (по столбцам)
        for col in range(cols):
            for row in range(rows - 1):
                current = row * cols + col
                next_vertex = current + cols
                edges.append((current, next_vertex))

        # Вызов конструктора родителя
        super().__init__(vertices, edges, color=(255, 255, 255))