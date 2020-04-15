import pygame
from app.modules.game import Game


WIDTH, HEIGHT = 1200, 800
FPS = 60
SCALE = 25

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

game = Game(screen, SCALE)

running = True

while running:
    delta_time = clock.get_time() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    game.update(delta_time)

    pygame.display.flip()

    clock.tick(FPS)


pygame.quit()
