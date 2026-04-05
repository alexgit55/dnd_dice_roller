"""Character class for the dice roller application"""

# This class will save character information and manage dice rolls

from character_traits import SavingThrows, Skills
from roll_manager import RollManager
from roll import Roll


class Character:
    """
    Represents a D&D character with ability scores, proficiency bonus, skills,
    saving throws
    Attributes:
        name (str): The character's name.
        ability_scores (dict): Mapping of ability names to their scores.
        proficiency_bonus (int): The character's proficiency bonus.
        save_bonus (int): Additional bonus to saving throws.
        skills (Skills): The character's skill proficiencies.
        saving_throws (SavingThrows): The character's saving throw
        proficiencies.
    Methods:
        set_ability_score(ability, score):
            Sets the score for a given ability.
        get_ability_score(ability):
            Retrieves the score for a given ability.
        calculate_ability_modifier(ability):
            Calculates the modifier for a given ability score.
        get_check_modifier(check, check_type="skill", weapon=None):
            Returns the modifier for a skill, saving throw, or attack check.
            - check: Name of the skill, saving throw, or weapon.
            - check_type: "skill", "save", or "attack".
            - weapon: Optional Weapon object for attack checks.
    """

    def __init__(self, name, character_id, ability_scores=None, proficiency_bonus=2, save_bonus=0):
        self.name = name
        self.character_id = character_id
        self.ability_scores = ability_scores if ability_scores else {}
        self.proficiency_bonus = proficiency_bonus
        self.save_bonus = save_bonus
        self.skills = Skills()
        self.saving_throws = SavingThrows()
        self.default_presets=RollManager()
        self.load_default_presets()

    def __repr__(self):
        return f"Character(name={self.name}, character_id={self.character_id})"

    def check_advantage(self, check_name, check_type="skill"):
        if check_type == "skill":
            return self.skills.has_advantage(check_name)
        elif check_type == "save":
            return self.saving_throws.has_advantage(check_name)
        else:
            return False

    def check_disadvantage(self, check_name, check_type="skill"):
        if check_type == "skill":
            return self.skills.has_disadvantage(check_name)
        elif check_type == "save":
            return self.saving_throws.has_disadvantage(check_name)
        else:
            return False

    def load_default_presets(self):
        self.default_presets.clear()

        skills_list = Skills.ability_map.keys()
        saves_list = SavingThrows.ability_map.keys()
        ability_list = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

        check_lists= {"skill": skills_list, "save": saves_list, "ability": ability_list}

        num_dice = 1
        dice_type = 'd20'

        for roll_type, check_list in check_lists.items():
            for name in check_list:
                dice_modifier = self.get_check_modifier(
                    check=name,
                    check_type=roll_type,
                )
                if self.check_advantage(check_name=name, check_type=roll_type):
                    advantage = "advantage_roll"
                elif self.check_disadvantage(check_name=name, check_type=roll_type):
                    advantage = "disadvantage_roll"
                else:
                    advantage = "normal_roll"
                roll = Roll(
                    num_dice=num_dice,
                    dice_type=dice_type,
                    dice_modifier=dice_modifier,
                    advantage=advantage,
                    name=name,
                    roll_type=roll_type
                )
                self.default_presets.add_roll(roll)

    def to_dict(self):
        return {
            "character_id": self.character_id,
            "name": self.name,
            "proficiency_bonus": self.proficiency_bonus,
            "save_bonus": self.save_bonus,
            "ability_scores": self.ability_scores,
            "skills": {
                "proficiencies": self.skills.get_proficiencies(),
                "advantages": self.skills.get_advantages(),
                "disadvantages": self.skills.get_disadvantages(),
            },
            "saving_throws": {
                "proficiencies": self.saving_throws.get_proficiencies(),
                "advantages": self.saving_throws.get_advantages(),
                "disadvantages": self.saving_throws.get_disadvantages(),
            },
        }

    @classmethod
    def from_dict(cls, data):
        character = cls(
            character_id=data["character_id"],
            name=data["name"],
            proficiency_bonus=data.get("proficiency_bonus", 2),
            save_bonus=data.get("save_bonus", 0),
            ability_scores=data.get("ability_scores", {}),
        )

        skills_data = data.get("skills", {})
        character.skills.set_proficiencies(skills_data.get("proficiencies", []))
        character.skills.set_advantages(skills_data.get("advantages", []))
        character.skills.set_disadvantages(skills_data.get("disadvantages", []))

        saves_data = data.get("saving_throws", {})
        character.saving_throws.set_proficiencies(saves_data.get("proficiencies", []))
        character.saving_throws.set_advantages(saves_data.get("advantages", []))
        character.saving_throws.set_disadvantages(saves_data.get("disadvantages", []))

        character.load_default_presets()

        return character

    def set_ability_score(self, ability, score):
        """Set an ability score for the character."""
        self.ability_scores[ability] = score

    def get_ability_score(self, ability):
        """Get an ability score for the character."""
        return self.ability_scores.get(ability, 0)

    def calculate_ability_modifier(self, ability):
        """Calculate the modifier for an ability score."""
        score = self.get_ability_score(ability)
        return (score - 10) // 2

    def get_check_modifier(self, check, check_type="skill"):
        """
        Get the modifier for a skill or saving throw.
        check: Name of the skill or saving throw.
        check_type: "skill" or "save".
        """
        ability = None
        is_proficient = False
        bonus = 0

        if check_type == "skill":
            ability = self.skills.ability_map.get(check)
            is_proficient = self.skills.is_proficient(check)
        elif check_type == "save":
            ability = self.saving_throws.ability_map.get(check)
            is_proficient = self.saving_throws.is_proficient(check)
            bonus += self.save_bonus
        elif check_type == "ability":
            ability = check


        if ability is not None:
            modifier = self.calculate_ability_modifier(ability)
        else:
            modifier = 0

        if is_proficient:
            modifier += self.proficiency_bonus

        return modifier + bonus


# Example usage
if __name__ == "__main__":
    John = Character(name="John", proficiency_bonus=4, character_id="2")
    John.saving_throws.set_proficiencies(["Strength", "Constitution"])
    John.skills.set_proficiencies(
        ["Animal Handling", "Athletics", "Intimidation", "Perception", "Survival"]
    )
    John.skills.set_advantages(["Deception", "Sleight of Hand"])
    John.saving_throws.set_advantages(["Dexterity", "Intelligence", "Wisdom", "Charisma"])
    John.saving_throws.set_disadvantages([])
    John.skills.set_disadvantages(["Stealth"])
    John.set_ability_score("Strength", 19)
    John.set_ability_score("Dexterity", 14)
    John.set_ability_score("Constitution", 18)
    John.set_ability_score("Intelligence", 9)
    John.set_ability_score("Wisdom", 12)
    John.set_ability_score("Charisma", 10)

    print(f"Character Name: {John.name}")
    print(f"Strength Modifier: {John.calculate_ability_modifier('Strength')}")
    print(f"Proficiency Bonus: {John.proficiency_bonus}")

    #John.load_default_presets()

    for preset in John.default_presets.rolls:
        print(preset)