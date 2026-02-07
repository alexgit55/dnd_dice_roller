import json
import os

class Roll:
    """
    Represents a dice roll configuration and its properties.

    This class is designed to encapsulate the details of a dice roll, including the
    number of dice, the type of dice, any modifiers, and additional options such as
    advantage rolls. It also provides utility methods for encoding and decoding roll
    objects into dictionary representations for serialization or deserialization
    purposes.

    :ivar name: The name or identifier for the dice roll.
    :type name: str
    :ivar num_dice: The number of dice to roll.
    :type num_dice: int
    :ivar dice_type: The type of dice being rolled (e.g., d6, d20).
    :type dice_type: str
    :ivar dice_modifier: A modifier to apply to the result of the roll (positive or
        negative).
    :type dice_modifier: int
    :ivar advantage: The type of roll advantage (e.g., 'normal_roll', 'advantage',
        'disadvantage').
    :type advantage: str
    """
    def __init__(self, num_dice, dice_type, dice_modifier, name='', advantage='normal_roll'):
        self.name = name
        self.num_dice = num_dice
        self.dice_type = dice_type
        self.dice_modifier = dice_modifier
        self.advantage = advantage

    def __repr__(self):
        if self.dice_modifier >=0:
            modifier_str = f"+{abs(self.dice_modifier)}"
        else:
            modifier_str = f"-{abs(self.dice_modifier)}"

        if self.advantage != 'normal_roll':
            return f"{self.name}: {self.num_dice}{self.dice_type}{modifier_str} ({self.advantage})"
        else:
            return f"{self.name}: {self.num_dice}{self.dice_type}{modifier_str}"

    @staticmethod
    def encode_roll(roll):
        """
        Encodes a `Roll` object into a dictionary representation.

        This method is responsible for converting a `Roll` instance into a
        dictionary using its attributes. The purpose of this is to facilitate
        serialization or further manipulation of the object. If the input is
        not a `Roll` instance, a `TypeError` is raised to ensure type safety.

        :param roll: The `Roll` object to be encoded.
        :type roll: Roll
        :return: A dictionary representation of the `Roll` object.
        :rtype: dict

        :raises TypeError: If the provided object is not an instance of `Roll`.
        """
        if isinstance(roll, Roll):
            return roll.__dict__
        else:
            raise TypeError("Object is not a Roll")

    @staticmethod
    def decode_roll(roll_dict):
        """
        Decodes a dictionary representation of a roll into a Roll object.

        This method takes a dictionary, where the information about a roll is stored,
        and converts it into an instance of a Roll object. It utilizes Python's
        unpacking mechanism and expects the dictionary keys to match the attributes
        of the Roll class.

        :param roll_dict: A dictionary containing information required to instantiate
            a Roll object.
        :type roll_dict: dict
        :return: An instance of the `Roll` class initialized with the data from
            `roll_dict`.
        :rtype: Roll
        """
        return Roll(**roll_dict)

class RollResult (Roll):
    """
    Represents the result of a dice roll operation with details on individual rolls,
    total, modifier, and formatting for display.

    This class extends functionality to encapsulate information about a dice roll,
    including its results, modifiers, and total values. The class is used to store
    and represent a roll's outcome in a structured and detailed manner.

    :ivar dice_total: The sum of the rolled dice values before applying the modifier.
    :type dice_total: int
    :ivar dice_rolls: The individual results of the dice rolls.
    :type dice_rolls: list[int]
    :ivar sign: The arithmetic sign (+ or -) based on the modifier.
    :type sign: str
    :ivar total: The final total after calculating dice sum and applying the modifier.
    :type total: int
    """
    def __init__(self, num_dice, dice_type, dice_rolls, dice_modifier, dice_total, advantage='normal_roll'):
        super().__init__(num_dice, dice_type, dice_modifier, advantage)
        self.dice_total = dice_total
        self.dice_rolls = dice_rolls
        self.sign = "+" if dice_modifier >= 0 else "-"
        self.total = dice_total + dice_modifier

    def __repr__(self):
        dice_shorthand=f"{self.num_dice}{self.dice_type}{self.sign}{abs(self.dice_modifier)}"
        if self.advantage != 'normal_roll':
            dice_details=f"{self.dice_rolls[0]} {self.dice_total}{self.sign}{abs(self.dice_modifier)} = {self.total}"
        else:
            if self.num_dice == 1:
                dice_details= f"{self.dice_total}{self.sign}{abs(self.dice_modifier)} = {self.total}"
            else:
                dice_details=f"{self.dice_rolls} {self.dice_total}{self.sign}{abs(self.dice_modifier)} = {self.total}"
        return f"{dice_shorthand}: {dice_details}"

class RollManager:
    """
    Manages a collection of rolls, providing functionality for adding, retrieving,
    updating, deleting, and persisting rolls.

    The RollManager class is designed to handle a collection of roll objects with
    methods to manage and process the rolls. It supports operations such as retrieving
    rolls by index, updating specific rolls, removing rolls, clearing the collection,
    and saving/loading rolls to/from a file.

    :ivar rolls: A list storing all the roll objects within the manager.
    :type rolls: list
    """
    def __init__(self):
        self.rolls = []

    def add_roll(self, roll):
        """
        Adds a roll to the list of rolls.

        This method appends the provided roll to the `rolls` list, allowing additional
        roll values to be tracked and stored.

        :param roll: The roll value to be added to the list of rolls.
        :type roll: Any
        """
        self.rolls.append(roll)

    def get_rolls(self):
        """
        Retrieves the list of rolls.

        This method provides access to the `rolls` attribute, which is expected to
        be a collection representing rolls. The rolls could refer to any application-
        specific use case, such as dice rolls, user roles, or similar data.

        :return: The list of rolls.
        :rtype: list
        """
        return self.rolls

    def get_roll(self, index):
        """
        Retrieves the roll corresponding to the provided index.

        This method accesses the `rolls` list and attempts to fetch the roll
        at the specified index. If the index is out of range, an
        IndexError is raised.

        :param index: The position in the `rolls` list to retrieve the roll.
        :type index: int
        :return: The roll at the specified index.
        :rtype: object
        :raises IndexError: If the provided index is out of the valid range for the `rolls` list.
        """
        try:
            return self.rolls[index]
        except IndexError:
            raise IndexError("Roll index out of range")

    def get_roll_index(self, roll):
        """
        Retrieves the index of a specified roll from the list of rolls.

        :param roll: The roll value to find in the list of rolls.
        :type roll: int or str
        :return: The index of the specified roll within the list of rolls.
        :rtype: int
        :raises ValueError: If the specified roll is not found in the list of rolls.
        """
        return self.rolls.index(roll)

    def update_roll(self, roll, index):
        """
        Updates the roll value at the specified index in the rolls list.

        This method modifies an element within the `rolls` list by replacing
        it with the provided `roll` value at the given `index`. It assumes that
        the `index` provided is valid and falls within the range of the list.

        :param roll: The new roll value to be updated in the list.
        :type roll: Any
        :param index: The index in the `rolls` list where the `roll` value should
                      be updated.
        :type index: int
        :return: This method does not return any value.
        :rtype: None
        """
        self.rolls[index] = roll

    def remove_roll(self, index):
        """
        Removes a roll from the list of rolls at the specified index.

        This function modifies the list of rolls by removing the roll located at the
        given index. The index must correspond to an existing element in the list.

        :param int index: The zero-based index of the roll to remove.
        :return: None
        """
        self.rolls.pop(index)

    def clear(self):
        """
        Clears all items in the `rolls` list.

        This method removes all elements from the `rolls` list, effectively resetting
        it to an empty state.

        :return: None
        """
        self.rolls.clear()

    def __len__(self):
        return len(self.rolls)

    def save_to_file(self, filename):
        """
        Saves the current rolls data to a specified JSON file. The rolls are
        encoded using the `encode_roll` method of the `Roll` class, and the
        result is written to the file in a readable JSON format.

        :param filename: Name of the file where the data will be saved. The
            file will be created or overwritten if it already exists.
        :type filename: str
        :return: None
        """
        data_to_write = [Roll.encode_roll(roll) for roll in self.rolls]
        with open(f'{filename}', 'w', encoding='utf-8') as f:
            json.dump(data_to_write, f, indent=4)

    def load_from_file(self, filename):
        """
        Loads roll data from a specified JSON file and populates the current instance with the
        deserialized roll information.

        :param filename: The name of the JSON file to read and load roll data from.
        :type filename: str
        :return: None
        """
        self.clear()
        with open(f'{filename}', 'r', encoding='utf-8') as f:
            rolls_json = f.read()
        rolls_list = json.loads(rolls_json)
        self.rolls = [Roll.decode_roll(roll) for roll in rolls_list]

if __name__ == '__main__':
    roll_manager = RollManager()
    roll_list = [Roll(2, 'd20', 2, 'My Roll'),
                 Roll(1, 'd20', -2, 'My Other Roll'),
                 Roll(3, 'd6', 5, 'My Third Roll'),
                 Roll(1, 'd20', 6, 'My Final Roll', advantage='advantage_roll')]

    for roll in roll_list:
        roll_manager.add_roll(roll)

    # Save rolls to a JSON file
    roll_manager.save_to_file('presets.json')
