
from ui.ui_settings import UISettings
from character_store import CharacterStore
from ui.main_window import MainWindow
from application.dice_roll_app_controller import DiceRollAppController

if __name__ == '__main__':
    character_list = CharacterStore()
    character_list.load_characters()
    dice_roll_app_controller = DiceRollAppController()


    UISettings.apply_theme()
    window = MainWindow(character_list.get_character("Warryn"), dice_roll_app_controller)
    window.run()