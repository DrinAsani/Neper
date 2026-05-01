# NEPER (Python + Pygame Prototype)

NEPER is a modular 2D top-down neighborhood exploration prototype focused on movement, branching NPC dialogue, respect/reputation, missions, unlockable doors, collectibles, and simple clothing unlocks.

## Architecture (brief)
- `main.py` starts the game loop.
- `game/core.py` orchestrates loading data, running updates, interactions, dialogue, missions, and rendering.
- `game/dialogue.py` handles dialogue conditions/effects in a data-driven way.
- `game/map.py`, `game/npc.py`, `game/player.py` represent core world entities.
- `game/mission.py` manages quest states (`locked`, `active`, `completed`).
- `game/inventory.py` stores long-lived progression state (respect, flags, items, clothes, doors).
- `game/ui.py` renders HUD + dialogue UI.
- `data/*.json` files hold content (maps, NPCs, dialogues, missions, collectibles, clothes).

## Install
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

## Run
```bash
python main.py
```

## Controls
- `WASD` / Arrow keys: move
- `E`: interact with nearby NPC
- `Space` / `Enter`: confirm dialogue choice
- `1/2/3` or Up/Down: choose dialogue options
- `Esc`: quit

## Current MVP Content
- Maps: `house`, `elevator`, `street`
- NPCs: Mom, Super D, Ray
- Branching dialogues with conditions/effects
- Respect system affects door unlock and choices
- 3 collectibles
- 1 mission (`errand_run`) with completion flow
- 1 locked door requiring reputation/respect
- 1 clothing unlock (`hoodie`) reflected by player color

## Add a new NPC
1. Add NPC entry in `data/npcs.json` with `name`, `x`, `y`, `dialogue_id`.
2. Add NPC id to the target map's `npcs` list in `data/maps.json`.
3. Add matching dialogue tree in `data/dialogues.json`.

## Add a dialogue branch
1. In `data/dialogues.json`, add a new node under a dialogue.
2. In a choice, set `next` to that node key.
3. Optionally add `conditions` (e.g. `respect_gte`, `flag_set`, `item_owned`, `mission_completed`).
4. Optionally add `effects` (e.g. `add_respect`, `unlock_mission`, `unlock_clothing`, `unlock_door`, `set_flag`, `complete_mission`).

## Add a locked door
1. In `data/maps.json`, add a door object with:
   - `id`
   - `rect` `[x,y,w,h]`
   - `target_map`
   - `target_spawn`
   - `required_respect`
2. Optionally unlock via dialogue effect `unlock_door` with same `id`.

## Replace placeholders with real assets
- Keep data IDs the same.
- Swap rectangle rendering in `game/core.py` with sprite blits.
- Put your images in `assets/sprites/` and map art in `assets/maps/`.


## Player sprite
- The player now attempts to load `assets/sprites/player/tulla_sprite.png` as a 4x4 sprite sheet.
- Sheet layout expected:
  - Rows: `down`, `left`, `right`, `up`
  - Columns: `idle`, `walk1`, `walk2`, `walk3`
- White/near-white background pixels are treated as transparent (color-key + near-white alpha cleanup).
- Sprite render size is controlled by `PLAYER_SPRITE_SCALE` in `game/settings.py`.
- Scaling affects rendering only; collision/hitbox still uses the original player rectangle.
- Movement uses walk frames while idle uses the first column.
- If the sprite file is missing or fails to load, the game falls back to rectangle rendering without affecting collision logic.
