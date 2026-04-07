import json
from domain.roll import Roll

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

    def get_rolls_by_type(self, roll_type=None):
        """
        Retrieves the list of rolls.

        This method provides access to the `rolls` attribute, which is expected to
        be a collection representing rolls. The rolls could refer to any application-
        specific use case, such as dice rolls, user roles, or similar data.

        :return: The list of rolls.
        :rtype: list
        """
        if roll_type is None:
            return self.rolls
        else:
            return [roll for roll in self.rolls if roll.roll_type == roll_type]

    def get_rolls_by_character(self, character_id):
        """
        Retrieve all rolls associated with a given character.

        This method iterates through a collection of rolls and filters those that belong
        to the character specified by the given character ID.

        :param character_id: The unique identifier of the character whose rolls need to
            be retrieved.
        :return: A list of rolls associated with the character matching the provided
            character ID. Each roll represents an instance tied to the character.
        :rtype: list
        """
        return [roll for roll in self.rolls if roll.character_id == character_id]

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

    def save_to_file(self, filename='data/presets.json'):
        """
        Saves the current rolls data to a specified JSON file. The rolls are
        encoded using the `encode_roll` method of the `Roll` class, and the
        result is written to the file in a readable JSON format.

        :param filename: Name of the file where the data will be saved. The
            file will be created or overwritten if it already exists.
        :type filename: str
        :return: None
        """
        data_to_write = [Roll.encode_roll(roll) for roll in self.rolls if roll.roll_type == 'custom']
        with open(f'{filename}', 'w', encoding='utf-8') as f:
            json.dump(data_to_write, f, indent=4)

    def load_from_file(self, filename='data/presets.json'):
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