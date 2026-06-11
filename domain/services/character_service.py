from domain.models.character import Character
from storage.character_repository import CharacterRepository

class CharacterService:
    """
    Handles character CRUD operations and active character selection.
    """

    def __init__(self):
        self.characters = []
        self.active_character = None

    def load_characters(self, filename='data/characters.json'):
        self.characters = CharacterRepository.load_characters_from_file(filename)
        self.ensure_default_character(filename)

        if self.active_character is None:
            self.active_character = self.characters[0]

    def save_characters(self, filename='data/characters.json'):
        CharacterRepository.save_characters_to_file(self.characters, filename)

    def get_all_characters(self):
        return self.characters

    def get_character(self, character_id):
        return next(
            (
                character
                for character in self.characters
                if character.character_id == character_id
            ),
            None,
        )

    def add_character(self, character):
        self.characters.append(character)
        self.save_characters()

    def update_character(self, updated_character):
        for index, character in enumerate(self.characters):
            if character.character_id == updated_character.character_id:
                updated_character.load_default_presets()
                self.characters[index] = updated_character

                if (
                    self.active_character is not None
                    and self.active_character.character_id == updated_character.character_id
                ):
                    self.active_character = updated_character

                self.save_characters()
                return True

        return False

    def delete_character(self, character_id):
        character = self.get_character(character_id)

        if character is None:
            return False

        if character.character_id == Character.DEFAULT_CHARACTER_ID:
            return False

        self.characters.remove(character)

        if (
            self.active_character is not None
            and self.active_character.character_id == character_id
        ):
            self.active_character = self.get_default_character()

        self.save_characters()
        return True

    def set_active_character(self, character_id):
        character = self.get_character(character_id)

        if character is None:
            return False

        self.active_character = character
        return True

    def get_active_character(self):
        return self.active_character

    def get_default_character(self):
        return self.get_character(Character.DEFAULT_CHARACTER_ID)

    def ensure_default_character(self, filename='data/characters.json'):
        if self.get_default_character() is None:
            character = Character.create_default()
            character.load_default_presets()
            self.characters.insert(0, character)
            self.save_characters(filename)

if __name__ == "__main__":
    character_service = CharacterService()
    character_service.load_characters('C:\\Scripts\\Python\\dnd_dice_roller\\data\\characters.json')
    print(character_service.get_all_characters())