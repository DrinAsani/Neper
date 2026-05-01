import pygame
from game.settings import PLAYER_SIZE, PLAYER_SPEED


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.speed = PLAYER_SPEED
        self.direction = "down"
        self.is_moving = False
        self.animation_timer = 0.0
        self.animation_frame = 0

    def update(self, dt, walls):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])

        length = (dx * dx + dy * dy) ** 0.5
        if length:
            dx /= length
            dy /= length

        self._update_direction(dx, dy)
        self.is_moving = bool(length)
        self._update_animation(dt)

        self._move_axis(dx * self.speed * dt, 0, walls)
        self._move_axis(0, dy * self.speed * dt, walls)

    def _update_direction(self, dx, dy):
        if dx == 0 and dy == 0:
            return
        if abs(dx) > abs(dy):
            self.direction = "right" if dx > 0 else "left"
        else:
            self.direction = "down" if dy > 0 else "up"

    def _update_animation(self, dt):
        if not self.is_moving:
            self.animation_timer = 0.0
            self.animation_frame = 0
            return

        self.animation_timer += dt
        if self.animation_timer >= 0.12:
            self.animation_timer -= 0.12
            self.animation_frame = (self.animation_frame + 1) % 3

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
