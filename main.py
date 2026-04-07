
from ui.ui_settings import UISettings
from character_store import CharacterStore
from ui.main_window import MainWindow

if __name__ == '__main__':
    character_list = CharacterStore()
    character_list.load_characters()

    UISettings.apply_theme()
    window = MainWindow(character_list.get_character("Warryn"))
    window.run()