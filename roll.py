import json
import os

class Roll:
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
            modifier_str = f"{abs(self.dice_modifier)}"

        if self.advantage != 'normal_roll':
            return f"{self.name}: {self.num_dice}{self.dice_type}{modifier_str} ({self.advantage})"
        else:
            return f"{self.name}: {self.num_dice}{self.dice_type}{modifier_str}"

    @staticmethod
    def encode_roll(roll):
        if isinstance(roll, Roll):
            return roll.__dict__
        else:
            raise TypeError("Object is not a Roll")

    @staticmethod
    def decode_roll(roll_dict):
        return Roll(**roll_dict)

class RollResult (Roll):
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
    def __init__(self):
        self.rolls = []

    def add_roll(self, roll):
        self.rolls.append(roll)

    def get_rolls(self):
        return self.rolls

    def get_roll(self, index):
        try:
            return self.rolls[index]
        except IndexError:
            raise IndexError("Roll index out of range")

    def get_roll_index(self, roll):
        return self.rolls.index(roll)

    def remove_roll(self, index):
        self.rolls.pop(index)

    def clear(self):
        self.rolls.clear()

    def __len__(self):
        return len(self.rolls)

    def save_to_file(self, filename):
        data_to_write = [Roll.encode_roll(roll) for roll in self.rolls]
        with open(f'{filename}', 'w', encoding='utf-8') as f:
            json.dump(data_to_write, f, indent=4)

    def load_from_file(self, filename):
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
