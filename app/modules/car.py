import pygame
import numpy as np
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
from app.modules.input_manager import InputManager
from app.modules.graphics.rect import Rect


class Car:
    def __init__(self, x, y, angle=0.0, length=4, max_steering=np.pi / 6, max_acceleration=5.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.angle = angle

        self.width = 1
        self.height = 2
        self.length = length

        self.wheel_radius = 0.3
        self.wheel_width = 0.2

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

    def update(self, delta_time):
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

    def render(self, screen, scale):
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
