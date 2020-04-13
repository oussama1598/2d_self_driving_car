import pygame


class InputManager:
    def __init__(self):
        self.keys_map = {
            pygame.K_LEFT: 'left',
            pygame.K_RIGHT: 'right',
            pygame.K_UP: 'throttle',
            pygame.K_DOWN: 'brake',
            pygame.K_SPACE: 'e_brake'
        }

        self.left = 0
        self.right = 0
        self.throttle = 0
        self.brake = 0

    def update_inputs(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.keys_map.keys():
                setattr(self, self.keys_map[event.key], 1)

        if event.type == pygame.KEYUP:
            if event.key in self.keys_map.keys():
                setattr(self, self.keys_map[event.key], 0)
