import json

from domain.models.character import Character


class CharacterRepository:
    """
    Handles loading and saving Character objects to persistent storage.
    """

    @staticmethod
    def load_characters_from_file(filename='data/characters.json'):
        """
        Loads characters from the configured JSON file.
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                characters_json = file.read()
            characters_from_file = json.loads(characters_json)
            return [Character.from_dict(character) for character in characters_from_file]
        except FileNotFoundError:
            return []

        return [Character.from_dict(item) for item in data]

    @staticmethod
    def save_characters_to_file(characters, filename='data/characters.json'):
        """
        Saves the provided characters to the configured JSON file.
        """
        data = [character.to_dict() for character in characters]

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)