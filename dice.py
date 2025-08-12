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
    def __init__(self, sides):
        self.sides = sides

    def roll(self, min_roll=1):
        return random.randint(min_roll, self.sides)

class DiceRoller:
    def __init__(self):
        self.dice = []

    def add_dice(self, die):
        self.dice.append(die)

    def roll_all(self):
        return [die.roll() for die in self.dice]

def roll_dice(die_string):
    try:
        num_dice, die_type = die_string.split("d")
        num_dice = int(num_dice)
        die_type = int(die_type)
    except ValueError:
        raise ValueError("Invalid die string format. Use 'NdM' format.")

    roller = DiceRoller()
    for _ in range(num_dice):
        roller.add_dice(Dice(die_type))
    return roller.roll_all()

# Example usage
if __name__ == "__main__":
    result = roll_dice("4d6")
    print(result)