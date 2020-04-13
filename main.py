import os
import pygame
from app.modules.tack import Track
from app.modules.car import Car


WIDTH, HEIGHT = 1200, 800
FPS = 60
SCALE = 25

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True

track = Track('path.json')
car = Car(0, 0, track=track)

while running:
    delta_time = clock.get_time() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        car.inputs.update_inputs(event)

    car.update(delta_time)

    screen.fill((0, 0, 0))

    track.render(screen)
    pygame.draw.line(
        screen,
        (255, 255, 255),
        (0, HEIGHT / 2),
        (WIDTH, HEIGHT / 2)
    )

    pygame.draw.line(
        screen,
        (255, 255, 255),
        (WIDTH / 2, 0),
        (WIDTH / 2, HEIGHT)
    )

    car.render(screen, SCALE)
    pygame.display.flip()

    clock.tick(FPS)


pygame.quit()
