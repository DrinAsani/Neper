import json
import pygame

from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLORS, DATA_DIR, INTERACT_DISTANCE
from game.player import Player
from game.npc import NPC
from game.map import GameMap
from game.dialogue import DialogueEngine
from game.mission import MissionManager
from game.inventory import GameState
from game.ui import UI


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("NEPER")
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False

        self.state = GameState()
        self.ui = UI()

        self.maps_data = self._load_json("maps.json")
        self.dialogues = self._load_json("dialogues.json")
        self.npcs_data = self._load_json("npcs.json")
        self.collectibles_data = self._load_json("collectibles.json")
        self.missions_data = self._load_json("missions.json")

        self.missions = MissionManager(self.missions_data, self.state)
        self.dialogue_engine = DialogueEngine(self.dialogues, self.state, self.missions)

        self.current_map_id = "house"
        self.current_map = GameMap(self.current_map_id, self.maps_data[self.current_map_id])
        self.player = Player(80, 120)
        self.dialogue_state = None

    def _load_json(self, filename):
        with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def build_npcs(self):
        npcs = []
        for npc_id in self.current_map.npcs:
            n = self.npcs_data[npc_id]
            npcs.append(NPC(npc_id, n["name"], n["x"], n["y"], n["dialogue_id"], n.get("color", [255, 160, 60])))
        return npcs

    def get_near_npc(self, npcs):
        for npc in npcs:
            if self.player.rect.centerx - npc.rect.centerx == 0 and self.player.rect.centery - npc.rect.centery == 0:
                return npc
            if ((self.player.rect.centerx - npc.rect.centerx) ** 2 + (self.player.rect.centery - npc.rect.centery) ** 2) ** 0.5 < INTERACT_DISTANCE:
                return npc
        return None

    def try_collect(self):
        for item_id in list(self.current_map.collectibles):
            item = self.collectibles_data[item_id]
            rect = pygame.Rect(item["x"], item["y"], 16, 16)
            if self.player.rect.colliderect(rect) and item_id not in self.state.items:
                self.state.items.add(item_id)
                self.state.respect += item.get("respect_gain", 0)
                clothing = item.get("unlock_clothing")
                if clothing:
                    self.state.unlocked_clothes.add(clothing)

    def try_door_transition(self):
        for door in self.current_map.doors:
            rect = pygame.Rect(*door["rect"])
            if self.player.rect.colliderect(rect):
                required = door.get("required_respect", 0)
                if self.state.respect >= required or door.get("id") in self.state.unlocked_doors:
                    self.current_map_id = door["target_map"]
                    self.current_map = GameMap(self.current_map_id, self.maps_data[self.current_map_id])
                    self.player.rect.topleft = tuple(door["target_spawn"])
                return

    def start_dialogue(self, npc):
        root = self.dialogues[npc.dialogue_id]["start"]
        self.dialogue_state = {"npc": npc, "dialogue_id": npc.dialogue_id, "node_id": root, "selected": 0}

    def advance_dialogue(self, choice_idx):
        state = self.dialogue_state
        node = self.dialogue_engine.get_node(state["dialogue_id"], state["node_id"])
        choices = self.dialogue_engine.get_available_choices(node)
        if not choices:
            self.dialogue_state = None
            return
        choice = choices[choice_idx]
        self.dialogue_engine.apply_effects(choice.get("effects", []))
        next_node = choice.get("next")
        if next_node:
            state["node_id"] = next_node
            state["selected"] = 0
        else:
            self.dialogue_state = None

    def handle_events(self, npcs):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if self.dialogue_state:
                    node = self.dialogue_engine.get_node(self.dialogue_state["dialogue_id"], self.dialogue_state["node_id"])
                    choices = self.dialogue_engine.get_available_choices(node)
                    if not choices:
                        self.dialogue_state = None
                        continue
                    if event.key in (pygame.K_DOWN, pygame.K_s):
                        self.dialogue_state["selected"] = (self.dialogue_state["selected"] + 1) % len(choices)
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        self.dialogue_state["selected"] = (self.dialogue_state["selected"] - 1) % len(choices)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_e):
                        self.advance_dialogue(self.dialogue_state["selected"])
                    elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                        idx = event.key - pygame.K_1
                        if idx < len(choices):
                            self.advance_dialogue(idx)
                else:
                    if event.key == pygame.K_e:
                        npc = self.get_near_npc(npcs)
                        if npc:
                            self.start_dialogue(npc)

    def draw(self, npcs):
        self.screen.fill(self.current_map.floor_color)
        for wall in self.current_map.walls:
            pygame.draw.rect(self.screen, COLORS["wall"], wall)
        for door in self.current_map.doors:
            rect = pygame.Rect(*door["rect"])
            required = door.get("required_respect", 0)
            unlocked = self.state.respect >= required or door.get("id") in self.state.unlocked_doors
            pygame.draw.rect(self.screen, COLORS["door_open"] if unlocked else COLORS["door_locked"], rect)
        for item_id in self.current_map.collectibles:
            if item_id in self.state.items:
                continue
            item = self.collectibles_data[item_id]
            pygame.draw.rect(self.screen, COLORS["collectible"], (item["x"], item["y"], 16, 16))
        for npc in npcs:
            pygame.draw.rect(self.screen, npc.color, npc.rect)
        pcolor = (70, 180, 255) if self.state.current_clothing == "default" else (170, 90, 240)
        pygame.draw.rect(self.screen, pcolor, self.player.rect)

        prompt = ""
        near = self.get_near_npc(npcs)
        if near and not self.dialogue_state:
            prompt = f"Press E to talk with {near.name}"
        self.ui.draw_hud(self.screen, self.state.respect, self.missions.get_active_mission_text(), prompt, self.state.current_clothing)

        if self.dialogue_state:
            node = self.dialogue_engine.get_node(self.dialogue_state["dialogue_id"], self.dialogue_state["node_id"])
            choices = self.dialogue_engine.get_available_choices(node)
            self.ui.draw_dialogue(self.screen, self.dialogue_state["npc"].name, node["text"], choices, self.dialogue_state["selected"])

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            npcs = self.build_npcs()
            self.handle_events(npcs)
            if not self.dialogue_state:
                self.player.update(dt, self.current_map.walls)
                self.try_collect()
                self.try_door_transition()
                if "hoodie" in self.state.unlocked_clothes:
                    self.state.current_clothing = "hoodie"
            self.draw(npcs)

        pygame.quit()
