import pygame

from game.settings import (
    PLAYER_SIZE,
    PLAYER_SPEED,
    PLAYER_SPRITE_PATH,
    PLAYER_SPRITE_COLS,
    PLAYER_SPRITE_ROWS,
    PLAYER_SCALE,
    PLAYER_ANIM_FPS,
)


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.speed = PLAYER_SPEED

        self.is_moving = False
        self.facing_row = 0  # 0 down, 1 left, 2 right, 3 up
        self.walk_frame_idx = 0
        self.anim_timer = 0.0
        self.frames = self._load_sprite_frames()

        if self.frames:
            self.draw_size = self.frames[0][0].get_size()
        else:
            self.draw_size = (PLAYER_SIZE, PLAYER_SIZE)

    def _load_sprite_frames(self):
        if not PLAYER_SPRITE_PATH.exists():
            return None
        try:
            sheet = pygame.image.load(str(PLAYER_SPRITE_PATH)).convert_alpha()
            sheet_w, sheet_h = sheet.get_size()
            frame_w = sheet_w // PLAYER_SPRITE_COLS
            frame_h = sheet_h // PLAYER_SPRITE_ROWS
            if frame_w <= 0 or frame_h <= 0:
                return None
            rows = []
            for row in range(PLAYER_SPRITE_ROWS):
                row_frames = []
                for col in range(PLAYER_SPRITE_COLS):
                    src = pygame.Rect(col * frame_w, row * frame_h, frame_w, frame_h)
                    frame = sheet.subsurface(src).copy()
                    if PLAYER_SCALE != 1:
                        frame = pygame.transform.scale(frame, (frame_w * PLAYER_SCALE, frame_h * PLAYER_SCALE))
                    row_frames.append(frame)
                rows.append(row_frames)
            return rows
        except pygame.error:
            return None

    def update(self, dt, walls):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])

        length = (dx * dx + dy * dy) ** 0.5
        self.is_moving = length > 0
        if length:
            dx /= length
            dy /= length
            if abs(dx) > abs(dy):
                self.facing_row = 2 if dx > 0 else 1
            else:
                self.facing_row = 0 if dy > 0 else 3

        self._move_axis(dx * self.speed * dt, 0, walls)
        self._move_axis(0, dy * self.speed * dt, walls)

        self._update_animation(dt)

    def _update_animation(self, dt):
        if not self.frames:
            return
        if not self.is_moving:
            self.walk_frame_idx = 0
            self.anim_timer = 0.0
            return
        self.anim_timer += dt
        step = 1.0 / PLAYER_ANIM_FPS
        while self.anim_timer >= step:
            self.anim_timer -= step
            self.walk_frame_idx = (self.walk_frame_idx + 1) % 3  # 3 walking columns (1..3)

    def get_current_frame(self):
        if not self.frames:
            return None
        if not self.is_moving:
            return self.frames[self.facing_row][0]  # idle column
        return self.frames[self.facing_row][self.walk_frame_idx + 1]

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
