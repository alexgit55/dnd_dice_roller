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


class Die:
    """
    A class representing a die with a configurable number of sides and minimum roll value.
    Attributes:
        sides (int): The number of sides on the dice.
        min_roll (int): The minimum value that can be rolled (default is 1).
    Methods:
        roll():
            Rolls the dice and returns a random integer between min_roll and sides (inclusive).
    """

    dice_types = {
        "d4": 4,
        "d6": 6,
        "d8": 8,
        "d10": 10,
        "d12": 12,
        "d20": 20,
        "d100": 100,
    }

    @classmethod
    def get_dice_types(cls):
        """
        Returns a list of available dice types.

        Returns:
            list: A list of strings representing the available dice types.
        """
        return list(cls.dice_types.keys())

    def __init__(self, dice_type, min_roll=1):
        self.sides = Die.dice_types[dice_type]
        self.min_roll = min_roll

    def roll(self):
        """
        Rolls the dice and returns a random integer between min_roll and sides (inclusive).

        Returns:
            int: The result of the dice roll.
        """
        return random.randint(self.min_roll, self.sides)


class DiceRoller:
    """
    DiceRoller is a class for managing and rolling multiple dice.
    Attributes:
        dice (list): A list of dice objects currently managed by the roller.
    Methods:
        add_dice(die):
            Adds a die object to the roller.
        remove_dice():
            Removes the most recently added die from the roller.
        roll_all():
            Rolls all dice currently managed by the roller and returns their results as a list.
        clear_dice():
            Removes all dice from the roller.
        d20_roll(advantage=0):
            Rolls two 20-sided dice (d20) for advantage/disadvantage mechanics.
            Args:
                advantage (int): 1 for advantage (returns highest), 2 for disadvantage
                (returns lowest), 0 for normal (returns first roll).
            Returns:
                tuple: (list of rolls, selected roll based on advantage/disadvantage)
        total_roll():
            Rolls all dice and returns both the individual results and their sum.
            Returns:
                tuple: (list of rolls, sum of rolls)
    """

    def __init__(self):
        self.dice = []

    def add_dice(self, die):
        """
        Adds a die to the dice collection.

        Args:
            die: An instance representing a single die to be added to the collection.

        Returns:
            None
        """
        self.dice.append(die)

    def remove_dice(self):
        """
        Removes the last dice from the dice list.

        This method removes the most recently added dice from the `self.dice` list.
        If the list is empty, it will raise an IndexError.

        Raises:
            IndexError: If there are no dice to remove.
        """
        self.dice.pop()

    def roll_all(self):
        """
        Rolls all dice in the collection and returns a list of their results.

        Returns:
            list: A list containing the result of rolling each die in self.dice.
        """
        return [die.roll() for die in self.dice]

    def clear_dice(self):
        """
        Removes all dice from the current collection, resetting it to an empty state.
        """
        self.dice.clear()

    def d20_roll(self, advantage=0):
        """
        Rolls two 20-sided dice and returns the results based on advantage or disadvantage.

        Args:
            advantage (int, optional): Determines the type of roll.
                - 1: Roll with advantage (returns both rolls and the higher value).
                - 2: Roll with disadvantage (returns both rolls and the lower value).
                - Any other value: Normal roll (returns both rolls and the first roll).

        Returns:
            tuple: A tuple containing:
                - list: The results of both dice rolls.
                - int: The selected roll based on advantage/disadvantage/normal.
        """
        self.clear_dice()
        self.add_dice(Die("d20"))
        self.add_dice(Die("d20"))
        rolls = self.roll_all()
        match advantage:
            case 1:
                return rolls, max(rolls)
            case 2:
                return rolls, min(rolls)
            case _:
                self.remove_dice()
                return rolls, rolls[0]

    def total_roll(self):
        """
        Rolls all dice and returns a tuple containing the list of individual
        dice rolls and their total sum.

        Returns:
            tuple: A tuple where the first element is a list of integers representing
                   the result of each die roll,
                   and the second element is an integer representing the sum of all dice rolls.
        """
        dice_rolls = self.roll_all()
        return dice_rolls, sum(dice_rolls)


# Example usage
if __name__ == "__main__":
    check = DiceRoller()
    check.add_dice(Die(6))
    check.add_dice(Die(6))
    result = check.d20_roll(advantage=2)
    print(result)
