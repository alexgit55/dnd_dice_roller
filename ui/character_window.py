import FreeSimpleGUI as sg

from ui.character_window_layout import build_layout, ABILITY_NAMES
from domain.models.character import Character
from domain.models.character_traits import SavingThrows, Skills

class CharacterWindow:
    """
    Represents a graphical user interface for viewing and editing character details.

    This class encapsulates the creation of a character editing window using a third-party GUI library.
    It provides functionality to build and collect character data based on user input and close the
    window when operations are complete.

    :ivar character: Holds the initial character data or None if no initial data is provided.
    :type character: Optional[Character]
    :ivar layout: Stores the layout of the GUI window.
    :type layout: Any
    :ivar window: Represents the GUI window object.
    :type window: Any
    """
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
        """
        Constructs a character object using the provided input values.

        This function processes the input dictionary to extract relevant details such as
        character name, proficiency bonus, ability scores, skill data, and saving
        throws data. It validates the mandatory fields and constructs the character
        object using the provided data.

        :param values: A dictionary containing all necessary fields to build a character.
                       Keys include the following:
                       - 'character_id': Unique identifier for the character.
                       - 'character_name': The name of the character.
                       - 'proficiency_bonus': Proficiency bonus of the character.
                       - 'save_bonus': Saving throw bonus of the character.
                       - 'ability_<ability_name>': Scores for different abilities (e.g., ability_STR, ability_DEX).
                       - 'skill_proficiencies': List of skills in which the character has proficiencies.
                       - 'skill_advantages': List of skills for which the character has advantages.
                       - 'skill_disadvantages': List of skills for which the character has disadvantages.
                       - 'save_proficiencies': List of saving throws in which the character has proficiencies.
                       - 'save_advantages': List of saving throws for which the character has advantages.
                       - 'save_disadvantages': List of saving throws for which the character has disadvantages.

        :type values: dict

        :return: An instance of the `Character` class built from the provided data.
                 Returns `None` if validation fails (e.g., missing character name).
        :rtype: Character or None
        """
        character_name = values["character_name"].strip()

        if not character_name:
            sg.popup_ok("Character name is required.")
            return None

        skill_proficiencies = []
        skill_expertise = []
        skill_advantages = []
        skill_disadvantages = []

        for skill_name in Skills.ability_map.keys():
            if values[f"skill_prof_proficient_{skill_name}"]:
                skill_proficiencies.append(skill_name)
            elif values[f"skill_prof_expertise_{skill_name}"]:
                skill_expertise.append(skill_name)

            if values[f"skill_adv_advantage_{skill_name}"]:
                skill_advantages.append(skill_name)
            elif values[f"skill_adv_disadvantage_{skill_name}"]:
                skill_disadvantages.append(skill_name)

        save_proficiencies = []
        save_advantages = []
        save_disadvantages = []

        for save_name in SavingThrows.ability_map.keys():
            if values[f"save_prof_proficient_{save_name}"]:
                save_proficiencies.append(save_name)

            if values[f"save_adv_advantage_{save_name}"]:
                save_advantages.append(save_name)
            elif values[f"save_adv_disadvantage_{save_name}"]:
                save_disadvantages.append(save_name)

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
                "proficiencies": skill_proficiencies,
                "expertise": skill_expertise,
                "advantages": skill_advantages,
                "disadvantages": skill_disadvantages,
            },
            "saving_throws": {
                "proficiencies": save_proficiencies,
                "advantages": save_advantages,
                "disadvantages": save_disadvantages,
            },
        }

        return Character.from_dict(character_data)


if __name__ == "__main__":
    window = CharacterWindow()
    window.run()