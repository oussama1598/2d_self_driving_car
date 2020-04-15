from app.modules.track import Track
from app.modules.car import Car


class Game:
    def __init__(self, screen, scale=1, cars_per_generation=1):
        self.screen = screen
        self.scale = scale
        self.cars_per_generation = cars_per_generation

        self.current_generation = 0
        self.current_cars = []

        self.track = Track('path.json')

        self._setup_first_generation()

    def _setup_first_generation(self):
        starting_x = self.track.starting_point[0] / self.scale
        starting_y = self.track.starting_point[1] / self.scale

        for i in range(self.cars_per_generation):
            self.current_cars.append(
                Car(starting_x, starting_y, game=self, track=self.track)
            )

    def remove(self, car):
        if car in self.current_cars:
            self.current_cars.remove(car)

    def update(self, delta_time):
        self.track.render(self.screen)

        for i in range(len(self.current_cars)):
            self.current_cars[i].render(
                self.screen,
                delta_time,
                self.scale
            )

        if len(self.current_cars) == 0:
            self._setup_first_generation()
