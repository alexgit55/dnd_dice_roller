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

    def get_proficiencies(self):
        """
        Retrieves the proficiencies associated with the object.

        :return: A list or other iterable containing the proficiencies of the object.
        :rtype: list
        """
        return self.proficiencies

    def set_proficiencies(self, proficiencies):
        """
        Sets the proficiencies for the instance.

        Args:
            proficiencies (list or any): The proficiencies to assign to the instance.
        """
        self.proficiencies = proficiencies

    def get_advantages(self):
        """
        Retrieves the advantages associated with the instance.

        :return: The list of advantages.
        :rtype: list
        """
        return self.advantages

    def set_advantages(self, advantages):
        """
        Sets the advantages for the current instance.

        Args:
            advantages (Any): The advantages to be assigned to the instance.
        """
        self.advantages = advantages

    def get_disadvantages(self):
        """
        Retrieves the disadvantages associated with the instance.

        This method returns a value, which represents the disadvantages
        present in the context of the implemented logic.

        :return: The disadvantages of the instance.
        :rtype: Any
        """
        return self.disadvantages

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
        "Survival": "Wisdom",
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
        "Charisma": "Charisma",
    }


if __name__ == "__main__":
    print(Skills.ability_map)