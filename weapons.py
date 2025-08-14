"""
This module defines the Weapon class, which represents a weapon in the D&D game.
Classes:
    Weapon: Represents a weapon with its properties and methods.
Example:
    sword = Weapon("Longsword", "martial", "slashing", 1d8, 15, 2)
    sword.attack()
"""

class Weapon:
    """
    Represents a weapon in a Dungeons & Dragons style dice roller.
    Attributes:
        name (str): The name of the weapon.
        category (str): The category of the weapon (e.g., melee, ranged).
        damage_type (str): The type of damage the weapon deals (e.g., slashing, piercing).
        damage (int): The base damage value of the weapon.
        ability (str): The primary ability used for attack rolls (default is "Strength").
        damage_bonus (int): Additional bonus damage (default is 0).
        weight_type (str): The weight classification of the weapon (default is "normal").
    Methods:
        attack():
            Prints the attack action and total damage dealt with the weapon.
        __str__():
            Returns a string representation of the weapon's attributes.
    """
    def __init__(
        self, name, category, damage_type,
        damage, ability="Strength", weight_type="normal"):

        self.name = name
        self.category = category
        self.damage_type = damage_type
        self.damage = damage
        self.ability = ability
        self.damage_bonus = 0
        self.weight_type = weight_type

    def __str__(self):
        return (f"Weapon: {self.name}, Category: {self.category}, "
                f"Damage Type: {self.damage_type}, Damage: {self.damage}, "
                f"Damage Bonus: {self.damage_bonus}, "
                f"Primary Ability: {self.ability}")

# Weapon Examples
if __name__ == "__main__":
    sword = Weapon("Longsword", "martial", "slashing", "1d8")
    bow = Weapon("Longbow", "martial", "piercing", "1d8", "Dexterity")
    dagger = Weapon("Dagger", "simple", "piercing", "1d4", "Dexterity")
