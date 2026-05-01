import pygame
from game.settings import PLAYER_SIZE, PLAYER_SPEED


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.speed = PLAYER_SPEED

    def update(self, dt, walls):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])

        length = (dx * dx + dy * dy) ** 0.5
        if length:
            dx /= length
            dy /= length

        self._move_axis(dx * self.speed * dt, 0, walls)
        self._move_axis(0, dy * self.speed * dt, walls)

    def _move_axis(self, dx, dy, walls):
        self.rect.x += int(dx)
        self.rect.y += int(dy)
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0:
                    self.rect.right = wall.left
                if dx < 0:
                    self.rect.left = wall.right
                if dy > 0:
                    self.rect.bottom = wall.top
                if dy < 0:
                    self.rect.top = wall.bottom
