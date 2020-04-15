import copy
import random
import pygame
import numpy as np
from app.modules.neural_network import NeuralNetwork
from app.modules.track import Track
from app.modules.car import Car


class Game:
    def __init__(self, screen, scale=1, cars_per_generation=80):
        self.screen = screen
        self.scale = scale

        self.number_of_cars_at_time = 6

        # font for the stats
        self.font = pygame.font.SysFont(None, 20)

        # fitness multiplyers
        self.check_points_multiplyer = 1.4
        self.time_multiplyer = .2
        self.sensors_multiplyer = .1

        # Genetic algorithm configuration
        self.cars_per_generation = cars_per_generation
        self.mutation_rate = 0.05  # 5% of randomizing
        # number of agents that are going to get selected from the most fit cars
        self.best_agents_selection = 8
        # number of agents that are going to get selected from the worst fit cars
        self.worst_agents_selection = 3
        # how much agents to cross over the rest well be randomized
        self.number_to_cross_over = 40

        self.current_generation = 1
        self.population = []

        self.current_cars = []
        self.playing_cars = []

        self.track = Track('path.json')

        self._setup_first_generation()

    def _setup_first_generation(self):
        starting_x = self.track.starting_point[0] / self.scale
        starting_y = self.track.starting_point[1] / self.scale

        for i in range(self.cars_per_generation):
            self.current_cars.append(
                Car(starting_x, starting_y, game=self,
                    track=self.track, manual=False)
            )

    def _render_stats(self):
        text = self.font.render(
            f'Generation: {self.current_generation}, Number of cars left: {len(self.current_cars)}',
            True,
            (255, 255, 255)
        )
        textRect = text.get_rect()
        textRect.center = (textRect.width / 2, textRect.height / 2)

        self.screen.blit(text, textRect)

    def _increase_generation(self):
        starting_x = self.track.starting_point[0] / self.scale
        starting_y = self.track.starting_point[1] / self.scale

        self.current_generation += 1

        genes_pool = []

        np_population = np.array(self.population)

        population = np_population[
            np_population[:, 0].argsort()
        ]

        # Filling the genes pool
        for fitness, neural_network in population[:self.best_agents_selection]:
            number_of_times = int(fitness * 10)

            for i in range(number_of_times):
                genes_pool.append(
                    copy.deepcopy(neural_network)
                )

        for fitness, neural_network in population[-self.worst_agents_selection:-1]:
            number_of_times = int(fitness * 10)

            for i in range(number_of_times):
                genes_pool.append(
                    copy.deepcopy(neural_network)
                )

        # Cross over the networks
        for i in range(self.number_to_cross_over):
            first_parent = random.choice(genes_pool)
            second_parent = None

            while second_parent == None or first_parent == second_parent:
                second_parent = random.choice(genes_pool)

            car = Car(starting_x, starting_y, game=self,
                      track=self.track, manual=False)

            car.neural_network.merge(
                first_parent, second_parent, mutation_rate=self.mutation_rate)

            self.current_cars.append(car)

        for i in range(self.cars_per_generation - self.number_to_cross_over):
            self.current_cars.append(
                Car(starting_x, starting_y, game=self,
                    track=self.track, manual=False)
            )

    def remove(self, car):
        if car in self.current_cars:
            self.population.append(
                [car.fitness, copy.deepcopy(car.neural_network)])
            self.current_cars.remove(car)
            self.playing_cars.remove(car)

    def update_inputs(self, event):
        for car in self.current_cars:
            car.inputs.update_inputs(event)

    def update(self, delta_time):
        self._render_stats()

        self.track.render(self.screen)

        if len(self.playing_cars) == 0:
            self.playing_cars = self.current_cars[:self.number_of_cars_at_time]

        for car in self.playing_cars:
            car.render(
                self.screen,
                delta_time,
                self.scale
            )

        if len(self.current_cars) == 0:
            self._increase_generation()
