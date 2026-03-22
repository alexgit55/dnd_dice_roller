"""Character class for the dice roller application"""

# This class will save character information and manage dice rolls

from character_traits import SavingThrows, Skills


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

    def __init__(self, name, ability_scores=None, proficiency_bonus=2):
        self.name = name
        self.ability_scores = ability_scores if ability_scores else {}
        self.proficiency_bonus = proficiency_bonus
        self.save_bonus = 0
        self.skills = Skills()
        self.saving_throws = SavingThrows()

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
    John = Character(name="John", proficiency_bonus=4)
    John.saving_throws.set_proficiencies(["Strength", "Constitution"])
    John.skills.set_proficiencies(
        ["Animal Handling", "Athletics", "Intimidation", "Perception", "Survival"]
    )
    John.set_ability_score("Strength", 19)
    John.set_ability_score("Dexterity", 14)
    John.set_ability_score("Constitution", 18)
    John.set_ability_score("Intelligence", 9)
    John.set_ability_score("Wisdom", 12)
    John.set_ability_score("Charisma", 10)

    print(f"Character Name: {John.name}")
    print(f"Strength Modifier: {John.calculate_ability_modifier('Strength')}")
    print(f"Proficiency Bonus: {John.proficiency_bonus}")
