from domain.services.dice_roll_service import DiceRollService

class DiceRollAppController:
    def __init__(self):
        self.dice_roll_service = DiceRollService()