import pygame
import numpy as np
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
from app.utils.math import check_intersection
from app.modules.input_manager import InputManager
from app.modules.graphics.rect import Rect
from app.modules.graphics.ray import Ray
from app.modules.neural_network import NeuralNetwork


class Car:
    def __init__(self, x, y, game=None, track=None, angle=0.0, length=4, max_steering=np.pi / 2, max_acceleration=5.0, manual=False):
        self.time = 0

        self.game = game

        self.neural_network = NeuralNetwork(
            inputs=7,
            outputs=2,
            hidden_layers=2,
            hidden_neurons=7
        )

        self.manual = False
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.angle = angle

        self.track = track

        self.width = .5
        self.height = 1
        self.length = length

        self.wheel_radius = 0.3 / 2
        self.wheel_width = 0.2 / 2

        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 20

        self.brake_deceleration = 10
        self.free_deceleration = 2

        self.acceleration_rate = 10

        self.acceleration = 0.0
        self.steering = 0.0

        self.last_position = None
        self.traveled_distance = 0

        # Input Manager
        self.inputs = InputManager()

        self.neural_network.show()

    def _do_physics(self, delta_time, steering, acceleration):
        # handle steering

        if self.manual:
            if self.inputs.right:
                self.steering -= (np.pi / 6) * delta_time
            elif self.inputs.left:
                self.steering += (np.pi / 6) * delta_time
            else:
                self.steering = 0

            self.steering = np.clip(
                self.steering,
                -self.max_steering,
                self.max_steering
            )

            if self.inputs.throttle:
                if self.velocity.x < 0:
                    self.acceleration = self.brake_deceleration
                else:
                    self.acceleration += self.acceleration_rate * delta_time

            elif self.inputs.brake:
                if self.velocity.x > 0:
                    self.acceleration = -self.brake_deceleration
                else:
                    self.acceleration -= self.acceleration_rate * delta_time

            else:
                if abs(self.velocity.x) > delta_time * self.free_deceleration:
                    self.acceleration = - \
                        np.abs(self.free_deceleration) * \
                        np.sign(self.velocity.x)
                else:
                    if delta_time != 0:
                        self.acceleration = -self.velocity.x / delta_time

            self.acceleration = np.clip(
                self.acceleration,
                -self.max_acceleration,
                self.max_acceleration
            )
        else:
            self.steering = steering * self.max_steering
            self.acceleration = acceleration * self.max_acceleration

        # integrate the position
        self.velocity.x += self.acceleration * delta_time

        # Restrain the velocity
        self.velocity.x = np.clip(
            self.velocity.x, -self.max_velocity, self.max_velocity)

        if self.steering:
            turning_radius = (self.length / 2) / sin(self.steering)
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(
            degrees(-self.angle)) * delta_time
        self.angle += angular_velocity * delta_time

    def _calculate_traveled_distance(self):
        if self.last_position:
            self.traveled_distance += np.linalg.norm(
                self.position - self.last_position)

        self.last_position = Vector2(self.position.x, self.position.y)

    def _check_wall_collisions(self, vertices):
        # construct car line edges
        segments = []

        for i in range(len(vertices)):
            vertex = vertices[i]
            next_vertex = vertices[i +
                                   1] if len(vertices) - 1 != i else vertices[0]

            segments.append((
                Vector2(*vertex),
                Vector2(*next_vertex)
            ))

        # Check the segments against the track for any intersection
        for cat_segment in segments:
            for track_segment in self.track.line_segments:
                intersection_point = check_intersection(
                    cat_segment,
                    track_segment
                )

                if len(intersection_point) > 0:
                    self.game.remove(self)

    def _shoot_rays(self, screen, scale):
        head_light_angle = np.arctan((self.width / 2) / (self.height / 2))

        rays_angles = [
            0,
            head_light_angle,
            -head_light_angle,
            np.pi / 2,
            -np.pi / 2,
            np.pi + head_light_angle,
            np.pi + -head_light_angle,
        ]

        intersection_points_per_rays = [[]
                                        for i in range(len(rays_angles))]
        distances = np.array([np.inf for i in range(len(rays_angles))])

        for i, ray_angle in enumerate(rays_angles):
            ray = Ray(
                0, 0,
                10
            )

            ray.rotate(self.angle + ray_angle)
            ray.translate(self.position.x, self.position.y)
            ray.render(screen, scale)

            # check for intersections
            for segment in self.track.line_segments:
                intersection_point = check_intersection(
                    segment,
                    (
                        Vector2(*ray.vertices[0]),
                        Vector2(*ray.vertices[1])
                    )
                )

                if len(intersection_point) > 0:
                    intersection_points_per_rays[i].append(intersection_point)

        for i, intersection_points in enumerate(intersection_points_per_rays):
            if len(intersection_points) == 0:
                continue

            points_distances = list(map(
                lambda point: np.linalg.norm((self.position * scale) - point),
                intersection_points
            ))
            nearest_point = intersection_points[np.argsort(points_distances)[
                0]]

            pygame.draw.circle(
                screen,
                (255, 255, 255),
                nearest_point.astype(int),
                5
            )

            # to normalize the distances to [0, 1]
            distances[i] = np.sort(points_distances)[0] / (10 * scale)

        return distances

    def render(self, screen, delta_time, scale):
        self.time += delta_time

        distances = self._shoot_rays(screen, scale)

        if self.manual:
            self._do_physics(delta_time, 0, 0)
        else:
            output = self.neural_network.predict(
                np.array([distances]))

            self._do_physics(delta_time, output[0][0], output[0][1])

        # Calculate traveled distance
        self._calculate_traveled_distance()

        # Creating graphics
        car_graphic = Rect(
            -self.height / 2, -self.width / 2,
            self.height, self.width
        )
        wheels = []

        for i in range(4):
            wheels.append(
                Rect(
                    -self.wheel_radius,
                    -self.wheel_width / 2,
                    self.wheel_radius * 2,
                    self.wheel_width,
                    color=(0, 255, 0)
                )
            )

        # positioning them
        car_graphic.rotate(self.angle)
        car_graphic.translate(self.position.x, self.position.y)
        car_graphic.render(screen, scale)

        # out of track detection
        self._check_wall_collisions(car_graphic.vertices)

        # rear wheels
        for wheel, side in zip(wheels[:2], [1, -1]):
            wheel.translate(-self.height / 2 +
                            self.wheel_radius, side * self.width / 2)
            wheel.rotate(self.angle)
            wheel.translate(self.position.x, self.position.y)
            wheel.render(screen, scale)

        # front wheels
        for wheel, side in zip(wheels[2:], [1, -1]):
            wheel.rotate(self.steering)
            wheel.translate(self.height / 2, side * self.width / 2)
            wheel.rotate(self.angle)
            wheel.translate(self.position.x, self.position.y)
            wheel.render(screen, scale)
