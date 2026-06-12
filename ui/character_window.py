import FreeSimpleGUI as sg

from ui.character_window_layout import build_layout, ABILITY_NAMES
from domain.models.character import Character

class CharacterWindow:
    def __init__(self, character=None):
        self.character = character
        self.layout = build_layout(character)
        self.window = sg.Window("Character Window", self.layout, finalize=True)

    def run(self):
        character = None
        while True:
            event, values = self.window.read()
            match event:
                case "save_character":
                    character = self.build_character_from_values(values)
                    if character is None:
                        continue
                    break
                case _ if event in (sg.WIN_CLOSED, "cancel", "exit"):
                    break

        self.window.close()
        return character

    def build_character_from_values(self, values):
        character_name = values["character_name"].strip()

        if not character_name:
            sg.popup_ok("Character name is required.")
            return None

        character_data = {
            "character_id": values["character_id"],
            "name": character_name,
            "proficiency_bonus": int(values["proficiency_bonus"]),
            "save_bonus": int(values["save_bonus"]),
            "ability_scores": {
                ability_name: int(values[f"ability_{ability_name}"])
                for ability_name in ABILITY_NAMES
            },
            "skills": {
                "proficiencies": values["skill_proficiencies"],
                "advantages": values["skill_advantages"],
                "disadvantages": values["skill_disadvantages"],
            },
            "saving_throws": {
                "proficiencies": values["save_proficiencies"],
                "advantages": values["save_advantages"],
                "disadvantages": values["save_disadvantages"],
            },
        }

        return Character.from_dict(character_data)


if __name__ == "__main__":
    window = CharacterWindow()
    window.run()