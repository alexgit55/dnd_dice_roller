from domain.services.dice_roll_service import DiceRollService
from domain.services.preset_service import PresetService


class DiceRollAppController:
    def __init__(self):
        self.dice_roll_service = DiceRollService()
        self.preset_service = PresetService()