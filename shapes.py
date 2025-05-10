import pygame
import numpy as np
from math import sqrt, sin, cos


class shape2D:
    def __init__(self, vertices: list, edges: list, color: tuple = (255, 255, 255)):
        self.color = color
        self.vertices = vertices  # List of (x, y) tuples
        self.edges = edges  # List of edge index pairs

    def calc_mean(self):
        sum_x = sum(v[0] for v in self.vertices)
        sum_y = sum(v[1] for v in self.vertices)
        return (sum_x / len(self.vertices), sum_y / len(self.vertices))

    def move(self, dx, dy):
        self.vertices = [(v[0] + dx, v[1] + dy) for v in self.vertices]

    def move_to(self, x, y):
        mean = self.calc_mean()
        self.move(x - mean[0], y - mean[1])

    def scale(self, s):
        mean = self.calc_mean()
        self.vertices = [
            ((v[0] - mean[0]) * s + mean[0],
             (v[1] - mean[1]) * s + mean[1])
            for v in self.vertices
        ]

    def rotate(self, angle):
        mean = self.calc_mean()
        cos_a, sin_a = cos(angle), sin(angle)
        new_vertices = []
        for v in self.vertices:
            dx = v[0] - mean[0]
            dy = v[1] - mean[1]
            new_x = dx * cos_a - dy * sin_a + mean[0]
            new_y = dx * sin_a + dy * cos_a + mean[1]
            new_vertices.append((new_x, new_y))
        self.vertices = new_vertices


class shape3D:
    def __init__(self, vertices: list, edges: list, faces: list, color: tuple = (255, 255, 255)):
        self.color = color
        self.vertices = vertices  # List of (x, y, z) tuples
        self.edges = edges  # List of edge index pairs
        self.faces = faces

    def calc_mean(self):
        sum_x = sum(v[0] for v in self.vertices)
        sum_y = sum(v[1] for v in self.vertices)
        sum_z = sum(v[2] for v in self.vertices)
        return (sum_x / len(self.vertices),
                sum_y / len(self.vertices),
                sum_z / len(self.vertices))

    def move(self, dx, dy, dz):
        self.vertices = [(v[0] + dx, v[1] + dy, v[2] + dz) for v in self.vertices]

    def move_to(self, x, y, z):
        mean = self.calc_mean()
        self.move(x - mean[0], y - mean[1], z - mean[2])

    def scale(self, s):
        mean = self.calc_mean()
        self.vertices = [
            ((v[0] - mean[0]) * s + mean[0],
             (v[1] - mean[1]) * s + mean[1],
             (v[2] - mean[2]) * s + mean[2])
            for v in self.vertices
        ]

    def rotate(self, angle_x=0, angle_y=0, angle_z=0):
        center = self.calc_mean()
        cos_x, sin_x = cos(angle_x), sin(angle_x)
        cos_y, sin_y = cos(angle_y), sin(angle_y)
        cos_z, sin_z = cos(angle_z), sin(angle_z)

        new_vertices = []
        for v in self.vertices:
            x = v[0] - center[0]
            y = v[1] - center[1]
            z = v[2] - center[2]

            if angle_x:
                y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x
            if angle_y:
                x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y
            if angle_z:
                x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z

            new_vertices.append((x + center[0], y + center[1], z + center[2]))

        self.vertices = new_vertices