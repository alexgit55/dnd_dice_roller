import json
from domain.character import Character

class CharacterStore:
    """
    Handles the storage, retrieval, and management of Character objects.

    This class is responsible for managing a collection of characters,
    saving them to a file, loading them from a file, and retrieving
    a specific character by name.

    :ivar filename: The name of the JSON file where characters are stored.
    :type filename: str
    :ivar characters: A list containing the Character objects.
    :type characters: List[Character]
    """
    def __init__(self, filename='data/characters.json'):
        self.filename = filename
        self.characters = []

    def save_characters(self):
        """
        Saves the list of characters to a file in JSON format.

        The method iterates over the characters, converting each to a dictionary
        representation, and then writes the resulting list of dictionaries to a
        JSON file.

        :return: None
        """
        data = [character.to_dict() for character in self.characters]
        with open(self.filename, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load_characters(self):
        """
        Loads character data from a JSON file and populates the ``characters`` attribute
        with instances of ``Character`` created from the data. If the file is not found,
        an empty list is returned and the ``characters`` attribute remains unchanged.

        :return: None if the file is successfully loaded and populated, otherwise returns
            an empty list if the file is not found.
        :rtype: Optional[list]
        """
        try :
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            return []

        self.characters = [Character.from_dict(item) for item in data]
        return None

    def get_character(self, name):
        """
        Retrieves a character from the list of characters by its name.

        :param name: The name of the character to retrieve.
        :type name: str
        :return: The character object with the specified name, or None if no
            such character exists.
        :rtype: Optional[Character]
        """
        selected_character = filter(lambda character: character.name == name, self.characters)
        return next(selected_character, None)

if __name__ == "__main__":
    store = CharacterStore()
    store.load_characters()

    for character in store.characters:
        print(character)