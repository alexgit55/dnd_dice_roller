class RollResult:
    def __init__(self, num_dice, dice_type, dice_rolls, dice_modifier, dice_total, advantage='normal_roll'):
        self.num_dice = num_dice
        self.dice_type = dice_type
        self.dice_modifier = dice_modifier
        self.dice_total = dice_total
        self.dice_rolls = dice_rolls
        self.advantage = advantage
        self.sign = "+" if dice_modifier >= 0 else "-"
        self.total = dice_total + dice_modifier

    def __repr__(self):
        dice_shorthand=f"{self.num_dice}{self.dice_type}{self.sign}{self.dice_modifier}"
        if self.advantage != 'normal_roll':
            dice_details=f"{self.dice_rolls[0]} {self.dice_total}{self.sign}{abs(self.dice_modifier)} = {self.total}"
        else:
            if self.num_dice == 1:
                dice_details= f"{self.dice_total}{self.sign}{abs(self.dice_modifier)} = {self.total}"
            else:
                dice_details=f"{self.dice_rolls} {self.dice_total}{self.sign}{abs(self.dice_modifier)} = {self.total}"
        return f"{dice_shorthand}: {dice_details}"

class RollHistory:
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

    def clear(self):
        self.rolls.clear()

    def __len__(self):
        return len(self.rolls)