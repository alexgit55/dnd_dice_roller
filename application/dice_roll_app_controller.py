from domain.services.dice_roll_service import DiceRollService
from domain.services.preset_service import PresetService
from domain.services.character_service import CharacterService
from domain.models.roll_history import RollHistory



class DiceRollAppController:
    def __init__(self):
        self.dice_roll_service = DiceRollService()
        self.preset_service = PresetService()
        self.roll_history = RollHistory()
        self.character_service = CharacterService()