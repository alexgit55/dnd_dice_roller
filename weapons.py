"""
This module defines the Weapon class, which represents a weapon in the D&D game.
Classes:
    Weapon: Represents a weapon with its properties and methods.
Example:
    sword = Weapon("Longsword", "martial", "slashing", 1d8, 15, 2)
    sword.attack()
"""

from dice import DiceRoller, Dice


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
        damage, ability="Strength", weight_type="normal",
        crit_score=20, damage_bonus=0, attack_bonus=0, damage_min=1):

        self.name = name
        self.category = category
        self.damage_type = damage_type
        self.damage = damage
        self.ability = ability
        self.damage_bonus = damage_bonus
        self.weight_type = weight_type
        self.crit_score = crit_score
        self.attack_bonus = attack_bonus
        self.damage_min = damage_min

    def __str__(self):
        return (f"Weapon: {self.name}, Category: {self.category}, "
                f"Damage Type: {self.damage_type}, Damage: {self.damage}, "
                f"Damage Bonus: {self.damage_bonus}, "
                f"Primary Ability: {self.ability}")

    def attack(self, attack_roll):
        """
        Simulates an attack with the weapon, rolling for damage and applying
        any relevant bonuses.
        """
        num_dice = int(self.damage[0])  # e.g., "2d6" -> 2
        die_type = self.damage[1:]  # e.g., "2d6" -> "d6"
        if attack_roll >= self.crit_score:
            num_dice *= 2
            
        damage_roller = DiceRoller()
        for _ in range(num_dice):
            die = Dice(die_type, self.damage_min)
            damage_roller.add_dice(die)
        return damage_roller.total_roll()

# Weapon Examples
if __name__ == "__main__":
    sword = Weapon("Longsword", "martial", "slashing", "1d8")
    bow = Weapon("Longbow", "martial", "piercing", "1d8", "Dexterity")
    dagger = Weapon("Dagger", "simple", "piercing", "1d4", "Dexterity")
