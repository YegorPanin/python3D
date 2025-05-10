import pygame

class camera:
    def __init__(self, screen, position=(0, 0), zoom=1.0):
        self.position = list(position)
        self.zoom = zoom
        self.update(screen)

    def update(self, screen):
        self.screen_rect = screen.get_rect()
        self.width = self.screen_rect.width
        self.height = self.screen_rect.height

    def project(self, vertices):
        """Проецирует 3D/2D вершины на экран"""
        projected = []
        half_w = self.width / 2
        half_h = self.height / 2

        for vertex in vertices:
            x = vertex[0]
            y = vertex[1]

            screen_x = (x - self.position[0]) * self.zoom + half_w
            screen_y = (y - self.position[1]) * self.zoom + half_h

            projected.append((screen_x, screen_y))

        return projected

    def draw(self, shape, surface):
        if not shape.vertices:
            return

        # 1. Проецируем вершины
        dots2d = self.project(shape.vertices)

        # 3. Рисуем рёбра
        if shape.edges: # Проверяем, есть ли информация о ребрах
            for edge in shape.edges:
                if len(edge) == 2:
                    start_index = edge[0]
                    end_index = edge[1]
                    if 0 <= start_index < len(dots2d) and 0 <= end_index < len(dots2d):
                         start = dots2d[start_index]
                         end = dots2d[end_index]
                         pygame.draw.line(surface, shape.color, start, end, 2)

        # 4. Рисуем вершины
        # Вершины обычно рисуются ПОСЛЕ ребер и граней
        for i, dot in enumerate(dots2d):
             pygame.draw.circle(surface, shape.color, (int(dot[0]), int(dot[1])), 4)

