import pygame
import numpy as np
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
from app.utils.math import check_intersection
from app.modules.input_manager import InputManager
from app.modules.graphics.rect import Rect
from app.modules.graphics.ray import Ray


class Car:
    def __init__(self, x, y, track=None, angle=0.0, length=4, max_steering=np.pi / 3, max_acceleration=5.0):
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

        self.acceleration_rate = 3

        self.acceleration = 0.0
        self.steering = 0.0

        # Input Manager
        self.inputs = InputManager()

    def _do_physics(self, delta_time):
        # handle steering

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
                    np.abs(self.free_deceleration) * np.sign(self.velocity.x)
            else:
                if delta_time != 0:
                    self.acceleration = -self.velocity.x / delta_time

        self.acceleration = np.clip(
            self.acceleration,
            -self.max_acceleration,
            self.max_acceleration
        )

        # integrate the position
        self.velocity.x += self.acceleration * delta_time

        # Restrain the velocity
        self.velocity.x = np.clip(
            self.velocity.x, -self.max_velocity, self.max_velocity)

        if self.steering:
            turning_radius = self.length / sin(self.steering)
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(
            degrees(-self.angle)) * delta_time
        self.angle += angular_velocity * delta_time

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
                    print('hit the wall')

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

        for ray_angle in rays_angles:
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
                    pygame.draw.circle(
                        screen,
                        (255, 255, 255),
                        intersection_point.astype(int),
                        5
                    )

    def render(self, screen, delta_time, scale):
        self._do_physics(delta_time)

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

        # self._shoot_rays(screen, scale)
