import os
import pygame
from math import copysign
from app.modules.car import Car

pygame.init()

WIDTH, HEIGHT = 800, 800
FPS = 60
SCALE = 25

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True

car = Car(0, 0)

current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "car.png")
car_image = pygame.image.load(image_path)

while running:
    delta_time = clock.get_time() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        car.inputs.update_inputs(event)

    car.update(delta_time)

    screen.fill((0, 0, 0))
    car.render(screen, SCALE)
    pygame.display.flip()

    clock.tick(FPS)


pygame.quit()
