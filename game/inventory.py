class GameState:
    """Holds progression/state values shared across systems."""

    def __init__(self):
        self.respect = 0
        self.flags = set()
        self.items = set()
        self.unlocked_clothes = {"default"}
        self.current_clothing = "default"
        self.unlocked_doors = set()
        self.missions = {}
