import pygame
from game.settings import NPC_SIZE


class NPC:
    def __init__(self, npc_id, name, x, y, dialogue_id, color=(255, 160, 60)):
        self.id = npc_id
        self.name = name
        self.rect = pygame.Rect(x, y, NPC_SIZE, NPC_SIZE)
        self.dialogue_id = dialogue_id
        self.color = tuple(color)
