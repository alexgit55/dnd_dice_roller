
from ui.ui_settings import UISettings
from ui.main_window import MainWindow
from application.dice_roll_app_controller import DiceRollAppController

if __name__ == '__main__':
    dice_roll_app_controller = DiceRollAppController()
    dice_roll_app_controller.character_service.load_characters()
    dice_roll_app_controller.preset_service.load_presets()

    UISettings.apply_theme()
    window = MainWindow(dice_roll_app_controller)
    window.run()