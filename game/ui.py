import pygame
from game.settings import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT


class UI:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont("arial", 20)
        self.small = pygame.font.SysFont("arial", 16)

    def draw_hud(self, screen, respect, mission_text, prompt, clothes):
        panel = pygame.Rect(0, 0, SCREEN_WIDTH, 70)
        pygame.draw.rect(screen, COLORS["ui_panel"], panel)
        screen.blit(self.font.render(f"Respect: {respect}", True, COLORS["ui_accent"]), (14, 10))
        screen.blit(self.font.render(f"Mission: {mission_text}", True, COLORS["ui_text"]), (14, 38))
        screen.blit(self.small.render(f"Outfit: {clothes}", True, COLORS["ui_text"]), (300, 12))
        if prompt:
            screen.blit(self.small.render(prompt, True, COLORS["ui_text"]), (300, 38))

    def draw_dialogue(self, screen, npc_name, text, choices, selected_idx):
        box = pygame.Rect(40, SCREEN_HEIGHT - 230, SCREEN_WIDTH - 80, 190)
        pygame.draw.rect(screen, (5, 5, 8), box)
        pygame.draw.rect(screen, (180, 180, 180), box, 2)
        screen.blit(self.font.render(npc_name, True, COLORS["ui_accent"]), (box.x + 12, box.y + 10))
        screen.blit(self.small.render(text, True, COLORS["ui_text"]), (box.x + 12, box.y + 42))
        for i, choice in enumerate(choices):
            color = COLORS["ui_accent"] if i == selected_idx else COLORS["ui_text"]
            msg = f"{i+1}. {choice['text']}"
            screen.blit(self.small.render(msg, True, color), (box.x + 12, box.y + 72 + 24 * i))
