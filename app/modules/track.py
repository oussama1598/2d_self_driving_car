import pygame
from pygame import Vector2
import json


class Track:
    def __init__(self, points_file):
        self.points_file = points_file

        self.outer_vertices = []
        self.inner_vertices = []
        self.starting_point = (0, 0)
        self.check_points = []
        self.line_segments = []

        self._load_points()
        self._construct_line_segments(self.outer_vertices)
        self._construct_line_segments(self.inner_vertices)

    def _load_points(self):
        with open(self.points_file, 'r') as file:
            points_data = json.loads(file.read())

            self.outer_vertices = points_data['outer_vertices']
            self.inner_vertices = points_data['inner_vertices']
            self.starting_point = points_data['starting_point']
            self.check_points = list(map(lambda points: [Vector2(
                *points[0]), Vector2(*points[1])], points_data['check_points']))

    def _construct_line_segments(self, vertices):
        for i in range(len(vertices)):
            vertex = vertices[i]
            next_vertex = vertices[i + 1] if i != len(
                vertices) - 1 else vertices[0]

            self.line_segments.append([
                Vector2(*vertex),
                Vector2(*next_vertex)
            ])

    def _render_path(self, screen, vertices, color=(255, 255, 255), poly_color=(255, 255, 255)):
        pygame.draw.polygon(
            screen,
            poly_color,
            vertices
        )

        for i in range(len(vertices)):
            vertex = vertices[i]
            next_vertex = vertices[i + 1] if i != len(
                vertices) - 1 else vertices[0]

            pygame.draw.circle(
                screen,
                color,
                vertex,
                3
            )

    def _render_check_points(self, screen, color=(255, 255, 255)):
        for segment in self.check_points:
            pygame.draw.line(
                screen,
                color,
                *segment
            )

    def render(self, screen):
        self._render_path(screen, self.outer_vertices, color=(
            255, 0, 0), poly_color=(169, 169, 169))
        self._render_path(screen, self.inner_vertices,
                          color=(0, 0, 255), poly_color=(0, 0, 0))
        self._render_check_points(screen)
