import json

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
    def __init__(self, num_dice, dice_type, dice_modifier,
                 name='', advantage='normal_roll', roll_type='custom',
                 character_id=None, **kwargs):
        self.name = name
        self.num_dice = num_dice
        self.dice_type = dice_type
        self.dice_modifier = dice_modifier
        self.advantage = advantage
        self.roll_type=roll_type
        self.character_id=character_id

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

    def get_shorthand(self):
        return f"{self.num_dice}{self.dice_type}{self.sign}{abs(self.dice_modifier)}"

    def __repr__(self):
        dice_shorthand=self.get_shorthand()
        if self.advantage != 'normal_roll':
            dice_details=f"{self.dice_rolls[0]} {self.dice_total}{self.sign}{abs(self.dice_modifier)} = {self.total}"
        else:
            if self.num_dice == 1:
                dice_details= f"{self.dice_total}{self.sign}{abs(self.dice_modifier)} = {self.total}"
            else:
                dice_details=f"{self.dice_rolls} {self.dice_total}{self.sign}{abs(self.dice_modifier)} = {self.total}"
        return f"{dice_shorthand}: {dice_details}"

if __name__ == '__main__':
    pass