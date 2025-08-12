"""
This module defines the Weapon class, which represents a weapon in the D&D game.
Classes:
    Weapon: Represents a weapon with its properties and methods.
Example:
    sword = Weapon("Longsword", "martial", "slashing", 1d8, 15, 2)
    sword.attack()
"""

class Weapon:
    def __init__(self, name, category, damage_type, damage, ability="Strength"):
        self.name = name
        self.category = category
        self.damage_type = damage_type
        self.damage = damage
        self.ability = ability
        self.damage_bonus = 0

    def attack(self):
        print(f"Attacking with {self.name} for {self.damage+self.damage_bonus} {self.damage_type} damage.")

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

    print(sword.attack())
    print(bow.attack())
    print(dagger.attack())
