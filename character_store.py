import json
from character import Character

class CharacterStore:
    def __init__(self, filename='characters.json'):
        self.filename = filename
        self.characters = []

    def save_characters(self):
        data = [character.to_dict() for character in self.characters]
        with open(self.filename, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load_characters(self):
        try :
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            return []

        self.characters = [Character.from_dict(item) for item in data]
        return None

    def get_character(self, name):
        selected_character = filter(lambda character: character.name == name, self.characters)
        return next(selected_character, None)

if __name__ == "__main__":
    store = CharacterStore()
    store.load_characters()

    for character in store.characters:
        print(character)