import numpy as np
from shapes import shape3D


class MengerSponge(shape3D):
    def __init__(self, level=2, color=(255, 255, 255)):
        self.level = level
        vertices, edges = self.generate_sponge(level)
        super().__init__(vertices, edges, color)

    def generate_cube(self, pos, size):
        """Генерация вершин и ребер куба"""
        x, y, z = pos
        s = size / 2

        vertices = [
            (x - s, y - s, z - s),
            (x + s, y - s, z - s),
            (x + s, y + s, z - s),
            (x - s, y + s, z - s),
            (x - s, y - s, z + s),
            (x + s, y - s, z + s),
            (x + s, y + s, z + s),
            (x - s, y + s, z + s)
        ]

        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]

        return vertices, edges

    def generate_sponge(self, level, pos=(0, 0, 0), size=1.0):
        """Рекурсивная генерация губки Менгера"""
        if level == 0:
            return self.generate_cube(pos, size)

        # Размер подкубов
        sub_size = size / 3
        sub_level = level - 1

        all_vertices = []
        all_edges = []
        index_offset = 0

        # Генерация 20 подкубов
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                for z in [-1, 0, 1]:
                    if (x == 0 and y == 0) or (x == 0 and z == 0) or (y == 0 and z == 0):
                        continue  # Пропускаем центральные кубы

                    # Позиция подкуба
                    sub_pos = (
                        pos[0] + x * sub_size,
                        pos[1] + y * sub_size,
                        pos[2] + z * sub_size
                    )

                    # Рекурсивная генерация
                    vs, es = self.generate_sponge(sub_level, sub_pos, sub_size)
                    all_vertices.extend(vs)

                    # Смещение индексов ребер
                    es = [(e[0] + index_offset, e[1] + index_offset) for e in es]
                    all_edges.extend(es)

                    index_offset += len(vs)

        return all_vertices, all_edges