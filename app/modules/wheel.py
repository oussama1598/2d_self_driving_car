import numpy as np
from app.modules.graphics.rect import Rect


class Wheel(Rect):
    def __init__(self, width, height, car=None, car_size=(10, 10), front=False, side='left'):
        super().__init__(color=(255, 0, 0))

        self.width = width
        self.height = height

        self.car = car

        self.car_width, self.car_height = car.width, car.height

        self.front = front
        self.side = side

    def draw(self, screen, scale):
        offset = np.array([
            -(self.car_width) / 2 if self.side == 'left' else (self.car_width / 2),
            -(self.car_height / 2) if self.front else (self.car_height / 2)
        ])

        self.position = np.copy(self.car.position) + offset

        if self.front:
            self.rotation = self.car.front_wheels_angle[
                0] if self.side == 'left' else self.car.front_wheels_angle[1]

        self.rotation += self.car.rotation

        super().draw(screen, scale)
