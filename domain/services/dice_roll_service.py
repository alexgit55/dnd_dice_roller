
from domain.models.roll import RollResult
from domain.models.dice import Die, DiceRoller

class DiceRollService:
    def __init__(self):
        self.roller = DiceRoller()

    @staticmethod
    def is_d20_roll(num_dice, dice_type):
        return num_dice == 1 and dice_type == 'd20'

    def roll_dice(self, num_dice, dice_type, dice_modifier, advantage):
        self.roller.clear_dice()

        if DiceRollService.is_d20_roll(num_dice, dice_type):
            rolls = self.roller.d20_roll(advantage)
            dice_total = rolls[1]
            roll_result = RollResult(num_dice, dice_type, rolls, dice_modifier, dice_total)
        else:
            for _ in range(num_dice):
                self.roller.add_dice(Die(dice_type))
                dice_total = self.roller.total_roll()
                roll_result = RollResult(num_dice, dice_type, dice_total[0], dice_modifier, dice_total[1])

        return roll_result