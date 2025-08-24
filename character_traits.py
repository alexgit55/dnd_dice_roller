"""Classes representing Skills and Saving Throws"""

class Checks:
    """
    Checks class manages proficiency, advantage, and disadvantage states for ability checks.
    Attributes:
        ability_map (dict): A mapping of ability names to their corresponding checks.
        proficiencies (list): List of checks the entity is proficient in.
        advantages (list): List of checks the entity has advantage on.
        disadvantages (list): List of checks the entity has disadvantage on.
    Methods:
        set_proficiencies(proficiencies):
            Sets the list of proficient checks.
        set_advantages(advantages):
            Sets the list of checks with advantage.
        set_disadvantages(disadvantages):
            Sets the list of checks with disadvantage.
        is_proficient(check):
            Returns True if the entity is proficient in the given check.
        has_advantage(check):
            Returns True if the entity has advantage on the given check.
        has_disadvantage(check):
            Returns True if the entity has disadvantage on the given check.
    """
    ability_map = {}

    def __init__(self):
        self.proficiencies = []
        self.advantages = []
        self.disadvantages = []

    def get_ability_list(self):
        """
        Returns a list of ability names available in the ability map.

        Returns:
            list: A list containing the keys (ability names) from the ability_map dictionary.
        """
        return list(self.ability_map.keys())

    def set_proficiencies(self, proficiencies):
        """
        Sets the proficiencies for the instance.

        Args:
            proficiencies (list or any): The proficiencies to assign to the instance.
        """
        self.proficiencies = proficiencies

    def set_advantages(self, advantages):
        """
        Sets the advantages for the current instance.

        Args:
            advantages (Any): The advantages to be assigned to the instance.
        """
        self.advantages = advantages

    def set_disadvantages(self, disadvantages):
        """
        Sets the disadvantages for the instance.

        Args:
            disadvantages (list): A list of disadvantages to assign.
        """
        self.disadvantages = disadvantages

    def is_proficient(self, check):
        """
        Determines if the specified check is in the list of proficiencies.

        Args:
            check (str): The name of the skill or save to check for proficiency.

        Returns:
            bool: True if the check is in self.proficiencies, False otherwise.
        """
        return check in self.proficiencies

    def has_advantage(self, check):
        """
        Determines if the specified check is in the list of advantages.

        Args:
            check (str): The name of the skill or save to check for advantage.

        Returns:
            bool: True if the check is in self.advantages, False otherwise.
        """
        return check in self.advantages

    def has_disadvantage(self, check):
        """
        Determines if the specified check is in the list of disadvantages.

        Args:
            check (str): The name of the skill or save to check for disadvantage.

        Returns:
            bool: True if the check is in self.disadvantages, False otherwise.
        """
        return check in self.disadvantages

class Skills(Checks):
    """
    Skills class maps D&D skill names to their corresponding ability scores.

    Attributes:
        ability_map (dict): Dictionary mapping skill names (str) to ability 
        scores (str).
            Example:
                "Acrobatics" -> "Dexterity"
                "Arcana" -> "Intelligence"
                "Stealth" -> "Dexterity"
                ...

    Inheritance:
        Inherits from Checks, which should provide common functionality for 
        skill checks.

    Usage:
        Use Skills.ability_map to look up which ability score is associated 
        with a given skill.
    """
    ability_map = {
        "Acrobatics": "Dexterity",
        "Animal Handling": "Wisdom",
        "Arcana": "Intelligence",
        "Athletics": "Strength",
        "Deception": "Charisma",
        "History": "Intelligence",
        "Insight": "Wisdom",
        "Intimidation": "Charisma",
        "Investigation": "Intelligence",
        "Medicine": "Wisdom",
        "Nature": "Intelligence",
        "Perception": "Wisdom",
        "Performance": "Charisma",
        "Persuasion": "Charisma",
        "Religion": "Intelligence",
        "Sleight of Hand": "Dexterity",
        "Stealth": "Dexterity",
        "Survival": "Wisdom"       
    }

class SavingThrows(Checks):
    """
    Represents saving throw checks for a character, mapping each saving throw 
    to its corresponding ability.

    Attributes:
        ability_map (dict): Maps saving throw names to their associated ability 
        scores.
    """
    ability_map = {
        "Strength": "Strength",
        "Dexterity": "Dexterity",
        "Constitution": "Constitution",
        "Intelligence": "Intelligence",
        "Wisdom": "Wisdom",
        "Charisma": "Charisma"
    }

class SpecialAbility:
    """
    Represents a special ability that can modify character traits such as attack, 
    damage, initiative, saving throws, and more.
    Attributes:
        ability_types (dict): Class-level dictionary mapping ability type keys to 
            their descriptions.
        name (str): The name of the special ability.
        ability_type (str): The type of ability, must be one of the keys in ability_types.
        bonus_value (int or float): The value of the bonus provided by the ability.
        is_active (bool): Indicates whether the ability is currently active.
    Methods:
        __init__(name, ability_type, bonus_value, is_active=False):
            Initializes a SpecialAbility instance with the given parameters.
            Raises KeyError if ability_type is not valid.
        activate():
            Activates the special ability.
        deactivate():
            Deactivates the special ability.
    """
    ability_types = {
        "attack_bonus": "Bonus to attack rolls.",
        "damage_bonus": "Bonus to damage rolls.",
        "initiative_bonus": "Bonus to initiative rolls.",
        "save_bonus": "Bonus to saving throws.",
        "dice_min": "Minimum roll value for damage dice.",
        "crit_score": "Critical hit score."
    }

    def __init__(
        self,
        name,
        ability_type,
        bonus_value,
        is_active=False
        ):

        self.name=name
        if ability_type in SpecialAbility.ability_types:
            self.ability_type=ability_type
        else:
            raise KeyError("Invalid Ability Type")
        self.bonus_value=bonus_value
        self.is_active=is_active

    def activate(self):
        """Activate the special ability."""
        self.is_active = True

    def deactivate(self):
        """Deactivate the special ability."""
        self.is_active = False
