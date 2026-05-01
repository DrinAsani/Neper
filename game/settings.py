from pathlib import Path

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
FPS = 60
TILE_SIZE = 32
PLAYER_SIZE = 24
PLAYER_SPEED = 180
NPC_SIZE = 24
COLLECTIBLE_SIZE = 16
INTERACT_DISTANCE = 48

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
ASSETS_DIR = ROOT_DIR / "assets"

# Player sprite sheet settings (4x4 grid)
PLAYER_SPRITE_PATH = ASSETS_DIR / "sprites" / "player" / "tulla_sprite.png"
PLAYER_SPRITE_COLS = 4
PLAYER_SPRITE_ROWS = 4
PLAYER_SCALE = 2
PLAYER_ANIM_FPS = 10

COLORS = {
    "bg": (20, 20, 28),
    "wall": (80, 80, 100),
    "floor_house": (45, 50, 60),
    "floor_elevator": (55, 55, 65),
    "floor_entrance": (35, 45, 40),
    "floor_street": (50, 50, 50),
    "player": (70, 160, 255),
    "npc": (255, 160, 60),
    "collectible": (250, 220, 70),
    "ui_panel": (10, 10, 12),
    "ui_text": (235, 235, 235),
    "ui_accent": (120, 220, 140),
    "door_locked": (160, 50, 50),
    "door_open": (70, 170, 90),
}
