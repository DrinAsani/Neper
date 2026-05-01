class DialogueEngine:
    def __init__(self, dialogue_data, game_state, mission_manager):
        self.dialogues = dialogue_data
        self.state = game_state
        self.missions = mission_manager

    def conditions_met(self, conditions):
        if not conditions:
            return True
        for cond in conditions:
            ctype = cond.get("type")
            if ctype == "respect_gte" and self.state.respect < cond.get("value", 0):
                return False
            if ctype == "flag_set" and cond.get("flag") not in self.state.flags:
                return False
            if ctype == "mission_completed" and self.state.missions.get(cond.get("mission_id")) != "completed":
                return False
            if ctype == "item_owned" and cond.get("item_id") not in self.state.items:
                return False
        return True

    def apply_effects(self, effects):
        for effect in effects or []:
            etype = effect.get("type")
            if etype == "add_respect":
                self.state.respect += effect.get("value", 0)
            elif etype == "set_flag":
                self.state.flags.add(effect.get("flag"))
            elif etype == "unlock_mission":
                self.missions.activate(effect.get("mission_id"))
            elif etype == "complete_mission":
                self.missions.complete(effect.get("mission_id"))
            elif etype == "unlock_door":
                self.state.unlocked_doors.add(effect.get("door_id"))
            elif etype == "unlock_clothing":
                self.state.unlocked_clothes.add(effect.get("clothing_id"))

    def get_node(self, dialogue_id, node_id):
        return self.dialogues[dialogue_id]["nodes"].get(node_id)

    def get_available_choices(self, node):
        choices = []
        for choice in node.get("choices", []):
            if self.conditions_met(choice.get("conditions", [])):
                choices.append(choice)
        return choices
