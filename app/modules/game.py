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
        self.distance_multiplyer = 1.4
        self.sensors_multiplyer = .1

        # Genetic algorithm configuration
        self.cars_per_generation = cars_per_generation
        self.mutation_rate = 0.1  # 10% of randomizing
        self.number_to_cross_over = 40

        self.current_generation = 1
        self.population = []

        self.current_cars = []
        self.playing_cars = []

        self.track = Track('path.json')

        self._setup_first_generation()

    def _get_random_color(self):
        r_color = np.linspace(0, 255, self.cars_per_generation)
        g_color = np.linspace(0, 255, self.cars_per_generation)
        b_color = np.linspace(0, 255, self.cars_per_generation)

        return (
            random.choice(r_color),
            random.choice(g_color),
            random.choice(b_color)
        )

    def _setup_first_generation(self):
        starting_x = self.track.starting_point[0] / self.scale
        starting_y = self.track.starting_point[1] / self.scale

        for i in range(self.cars_per_generation):
            r_color = np.linspace(0, 255, 80)[i]

            self.current_cars.append(
                Car(
                    starting_x,
                    starting_y,
                    color=self._get_random_color(),
                    game=self,
                    track=self.track,
                    manual=False
                )
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

    def _mutate(self, value):
        if np.random.uniform(0, 1) < self.mutation_rate:
            return np.random.uniform(-1.0, 1.0)

        return value

    def _merge(self, parent_1, parent_2, child1, child2):
        for i in range(child1.hidden_layers_number + 1):
            if np.random.uniform(0, 1) > .5:
                child1.biases[i] = self._mutate(parent_1.biases[i])
                child2.biases[i] = self._mutate(parent_2.biases[i])
            else:
                child1.biases[i] = self._mutate(parent_2.biases[i])
                child2.biases[i] = self._mutate(parent_1.biases[i])

            for j in range(len(child1.weights[i])):
                for k in range(len(child1.weights[i][j])):
                    if np.random.uniform(0, 1) > .5:
                        child1.weights[i][j][k] = self._mutate(
                            parent_1.weights[i][j][k])
                        child2.weights[i][j][k] = self._mutate(
                            parent_2.weights[i][j][k])
                    else:
                        child1.weights[i][j][k] = self._mutate(
                            parent_2.weights[i][j][k])
                        child2.weights[i][j][k] = self._mutate(
                            parent_1.weights[i][j][k])

    def _increase_generation(self):
        starting_x = self.track.starting_point[0] / self.scale
        starting_y = self.track.starting_point[1] / self.scale

        self.current_generation += 1

        genes_pool = []

        # Filling the genes pool
        for fitness, neural_network, color in self.population:
            number_of_times = int(fitness * 10)

            for i in range(number_of_times):
                genes_pool.append(
                    [copy.deepcopy(neural_network), color, fitness]
                )

        # Cross over the networks
        for i in range(self.number_to_cross_over):
            first_dna = random.choice(genes_pool)
            second_dna = None

            while second_dna == None or first_dna == second_dna:
                second_dna = random.choice(genes_pool)

            print('parent 1: ', first_dna[2])
            print('parent 2: ', second_dna[2])

            first_parent = first_dna[0]
            second_parent = second_dna[0]

            child_1 = Car(starting_x, starting_y, game=self,
                          track=self.track, manual=False)
            child_2 = Car(starting_x, starting_y, game=self,
                          track=self.track, manual=False)

            self._merge(first_parent, second_parent,
                        child_1.neural_network, child_2.neural_network)

            if np.random.uniform(0, 1) > .5:
                child_1.color = first_dna[1]
                child_2.color = second_dna[1]
            else:
                child_2.color = first_dna[1]
                child_1.color = second_dna[1]

            self.current_cars.append(child_1)
            self.current_cars.append(child_2)

        for i in range(self.cars_per_generation - (self.number_to_cross_over * 2)):
            self.current_cars.append(
                Car(starting_x, starting_y, color=self._get_random_color(), game=self,
                    track=self.track, manual=False)
            )

        self.population = []

    def remove(self, car):
        if car in self.current_cars:
            self.population.append(
                [car.fitness, copy.deepcopy(car.neural_network), car.color])
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
