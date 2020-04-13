import pygame
import numpy as np
from app.utils.math import rotate_vector


class Rect:
    def __init__(self, x, y, width, height, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.color = color

        self.vertices = [
            np.array([x, y]),
            np.array([x + width, y]),
            np.array([x + width, y + height]),
            np.array([x, y + height])
        ]

    def translate(self, x, y):
        for i in range(len(self.vertices)):
            self.vertices[i] += np.array([x, y])

    def rotate(self, angle):
        for i in range(len(self.vertices)):
            self.vertices[i] = rotate_vector(self.vertices[i], angle)

    def render(self, screen, scale):
        self.vertices = list(map(
            lambda vertex: vertex * scale,
            self.vertices
        ))

        pygame.draw.polygon(
            screen,
            self.color,
            self.vertices
        )
