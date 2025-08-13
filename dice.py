"""
dice.py
This module provides classes and functions for simulating dice rolls in a 
Dungeons & Dragons (D&D) context. It includes the Dice class for individual 
dice and the DiceRoller class for rolling multiple dice and calculating 
results.
Classes:
    Dice: Represents a single die with a specified number of sides.
    DiceRoller: Manages the rolling of multiple dice and the calculation of 
    their results.
Functions:
    roll_dice(die_string): Rolls a specified die and returns the result.
Example:
    result = roll_dice("2d6 + 3")
    print(result)
"""
import random

class Dice:
    def __init__(self,sides, min_roll=1):
        self.sides = sides
        self.min_roll = min_roll

    def roll(self):
        return random.randint(self.min_roll, self.sides)

class DiceRoller:
    def __init__(self):
        self.dice = []

    def add_dice(self, die):
        self.dice.append(die)
        
    def remove_dice(self):
        self.dice.pop()

    def roll_all(self):
        return [die.roll() for die in self.dice]

    def clear_dice(self):
        self.dice.clear()

    def d20_roll(self, advantage=0):
        self.clear_dice()
        self.add_dice(Dice(20))
        self.add_dice(Dice(20))
        rolls = self.roll_all()
        match advantage:
            case 1:
                return (rolls, max(rolls))
            case 2:
                return (rolls, min(rolls))
            case _:
                self.remove_dice()
                return (rolls, rolls[0])

# Example usage
if __name__ == "__main__":
    check = DiceRoller()
    check.add_dice(Dice(6))
    check.add_dice(Dice(6))
    result = check.d20_roll(advantage=2)
    print(result)