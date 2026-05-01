import pygame


class GameMap:
    def __init__(self, map_id, data):
        self.id = map_id
        self.name = data["name"]
        self.width = data["width"]
        self.height = data["height"]
        self.floor_color = tuple(data["floor_color"])
        self.walls = [pygame.Rect(*w) for w in data.get("walls", [])]
        self.doors = data.get("doors", [])
        self.collectibles = data.get("collectibles", [])
        self.npcs = data.get("npcs", [])
        self.player_start = data.get("player_start")
        self.decor = data.get("decor", {})
        self.decorations = data.get("decorations", [])
