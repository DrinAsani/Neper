class MissionManager:
    def __init__(self, mission_data, game_state):
        self.missions = mission_data
        self.state = game_state
        for mid, mission in mission_data.items():
            self.state.missions[mid] = mission.get("initial_state", "locked")

    def activate(self, mission_id):
        if mission_id in self.state.missions and self.state.missions[mission_id] == "locked":
            self.state.missions[mission_id] = "active"

    def complete(self, mission_id):
        if mission_id in self.state.missions:
            self.state.missions[mission_id] = "completed"

    def get_active_mission_text(self):
        for mid, status in self.state.missions.items():
            if status == "active":
                return self.missions[mid].get("title", mid)
        return "No active mission"
