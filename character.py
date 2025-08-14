"""Character class for the dice roller application"""
# This class will save character information and manage dice rolls

from skills_saves import SavingThrows, Skills


class Character:
    """
    Represents a D&D character with ability scores, proficiency bonus, skills, 
    saving throws, and weapons.
    Attributes:
        name (str): The character's name.
        ability_scores (dict): Mapping of ability names to their scores.
        proficiency_bonus (int): The character's proficiency bonus.
        damage_bonus (int): Additional bonus to damage rolls.
        save_bonus (int): Additional bonus to saving throws.
        skills (Skills): The character's skill proficiencies.
        saving_throws (SavingThrows): The character's saving throw 
        proficiencies.
        weapons (list): List of Weapon objects the character possesses.
    Methods:
        set_ability_score(ability, score):
            Sets the score for a given ability.
        get_ability_score(ability):
            Retrieves the score for a given ability.
        calculate_ability_modifier(ability):
            Calculates the modifier for a given ability score.
        add_weapon(weapon):
            Adds a weapon to the character's inventory, applying proficiency 
            bonus if weapon is heavy.
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
        self.damage_bonus = 0
        self.save_bonus = 0
        self.skills = Skills()
        self.saving_throws = SavingThrows()
        self.weapons = []

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

    def add_weapon(self, weapon):
        """
        Adds a weapon to the character's arsenal. If the weapon is of type 
        'Heavy', increases its damage bonus by the character's proficiency bonus 
        before adding.

        Args:
            weapon: An object representing the weapon to be added. Must have 
            'weight_type','damage_bonus', and support being appended to 
            self.weapons.
        """
        if weapon.weight_type == "Heavy":
            weapon.damage_bonus += self.proficiency_bonus
        self.weapons.append(weapon)

    def get_weapon_list(self):
        """
        Get a list of all weapons the character is proficient with.
        """
        return [weapon.name for weapon in self.weapons]

    def get_check_modifier(self, check, check_type="skill", weapon=None):
        """
        Get the modifier for a skill or saving throw.
        check: Name of the skill or saving throw.
        check_type: "skill" or "save".
        """
        ability = None
        is_proficient = False
        modifier = 0
        bonus = 0

        if check_type == "skill":
            ability = self.skills.ability_map.get(check)
            is_proficient = self.skills.is_proficient(check)
        elif check_type == "save":
            ability = self.saving_throws.ability_map.get(check)
            is_proficient = self.saving_throws.is_proficient(check)
            bonus += self.save_bonus
        elif check_type == "attack":
            # For weapon attacks, we assume proficiency is always true
            # Get the weapon that matches the name of the check variable
            weapon = next((w for w in self.weapons if w.name == check), None)
            if weapon:
                ability = weapon.ability
            is_proficient = True

        if ability is not None:
            modifier = self.calculate_ability_modifier(ability)
        else:
            modifier = 0

        if is_proficient:
            modifier += self.proficiency_bonus

        return modifier + bonus

# Example usage
if __name__ == "__main__":
    John = Character(name="John", proficiency_bonus=5)
    John.saving_throws.set_proficiencies(["Strength", "Constitution"])
    John.skills.set_proficiencies([
        "Animal Handling", "Athletics", "Intimidation", "Perception", "Survival"])
    John.set_ability_score("Strength", 20)
    John.set_ability_score("Dexterity", 14)
    John.set_ability_score("Constitution", 15)
    John.set_ability_score("Intelligence", 12)
    John.set_ability_score("Wisdom", 13)
    John.set_ability_score("Charisma", 10)

    print(f"Character Name: {John.name}")
    print(f"Strength Modifier: {John.calculate_ability_modifier('Strength')}")
    print(f"Proficiency Bonus: {John.proficiency_bonus}")
