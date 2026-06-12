from domain.models.character import Character
from storage.character_repository import CharacterRepository

class CharacterService:
    """
    Manages a collection of characters, allowing for loading, saving, and operations
    such as adding, updating, deleting, and retrieving characters.

    This service interacts with a character repository to persist characters in a
    file, assigns unique IDs to characters, and ensures a default character is
    always present. It also supports setting and retrieving the currently active
    character.

    :ivar characters: A collection of all loaded characters.
    :type characters: list[Character]
    :ivar active_character: The currently active character or None if no character
        is active.
    :type active_character: Character | None
    """
    def __init__(self):
        self.characters = []
        self.active_character = None

    def load_characters(self, filename='data/characters.json'):
        """
        Loads characters from a given JSON file and sets up the active character.

        This method reads characters from the specified file, populates the
        `characters` attribute with the loaded data, and ensures that a default
        character is available. Additionally, if no active character is set, it
        automatically assigns the first character in the list as the active one.

        :param filename: The file path to the JSON file containing character data.
                         Defaults to 'data/characters.json'.
        :return: None
        """
        self.characters = CharacterRepository.load_characters_from_file(filename)
        self.ensure_default_character(filename)

        if self.active_character is None:
            self.active_character = self.characters[0]

    def save_characters(self, filename='data/characters.json'):
        """
        Saves the character data to a specified file.

        The method utilizes the CharacterRepository to save the current list of
        characters to the file provided in the `filename` parameter. If no filename
        is specified, it defaults to 'data/characters.json'.

        :param filename: Path to the file where character data will be saved. Defaults
            to 'data/characters.json'.
        :type filename: str
        :return: None
        """
        CharacterRepository.save_characters_to_file(self.characters, filename)

    def get_next_character_id(self):
        """
        Gets the next available character ID using the c-### format.

        The default character is ignored. Existing IDs that do not match the
        expected c-### format are also ignored.

        Examples:
            default only -> c-001
            c-001 -> c-002
            c-001, c-004 -> c-005

        :return: The next available character ID.
        :rtype: str
        """
        highest_character_number = 0

        for character in self.characters:
            character_id = character.character_id

            if character_id == Character.DEFAULT_CHARACTER_ID:
                continue

            if not character_id.startswith("c-"):
                continue

            character_number = character_id.removeprefix("c-")

            if not character_number.isdigit():
                continue

            highest_character_number = max(
                highest_character_number,
                int(character_number),
            )

        next_character_number = highest_character_number + 1
        return f"c-{next_character_number:03}"

    def get_characters(self):
        """
        Retrieves the names of all characters.

        This method iterates through the `characters` attribute and collects the names of each
        character in the list. It returns a list containing the names of all characters found
        in the `characters` attribute.

        :return: A list of names of the characters.
        :rtype: list[str]
        """
        return [character.name for character in self.characters]

    def get_character_by_id(self, character_id):
        """
        Fetches a character by its unique identifier from the list of characters.

        This method iterates through the list of available characters and searches
        for the character with the specified unique identifier. It returns the
        corresponding character object if found; otherwise, it returns None.

        :param character_id: The unique identifier of the character to be retrieved.
        :type character_id: Any
        :return: The character object with the matching identifier, or None if no
            matching character is found.
        :rtype: Optional[Any]
        """
        return next(
            (
                character
                for character in self.characters
                if character.character_id == character_id
            ),
            None,
        )

    def get_character_by_name(self, character_name):
        """
        Retrieve a character by its name from the list of characters.

        This method iterates through the list of characters within the current
        object and returns the first character whose name matches the specified
        name. If no character with the given name is found, the method will
        return None.

        :param character_name: The name of the character to retrieve.
        :type character_name: str
        :return: The character matching the specified name, or None if not found.
        :rtype: Optional[Character]
        """
        return next(
            (
                character
                for character in self.characters
                if character.name == character_name
            ),
            None,
        )

    def add_character(self, character):
        """
        Adds a character to the character list and saves the updated list.

        :param character: The character to be added.
        :type character: Any
        :return: None
        """
        self.characters.append(character)
        self.save_characters()

    def update_character(self, updated_character):
        """
        Updates an existing character in the character list. If the character being updated
        matches the currently active character, updates the active character as well. Saves
        the updated list of characters to storage after the update.

        :param updated_character: The character object that contains updated data. Must have
            a `character_id` attribute which is used to identify and replace the correct
            character in the list.
        :type updated_character: Character
        :return: `True` if the character was successfully updated in the list; `False` if
            the character with the given ID was not found in the list.
        :rtype: bool
        """
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
        """
        Deletes a character by its unique identifier. The method ensures that the character
        is removed from the list if it exists and is not the default character. If the
        currently active character is the one being deleted, it is replaced by the default
        character.

        :param character_id: The unique identifier of the character to be deleted.
        :type character_id: int
        :return: A boolean indicating whether the character was successfully deleted.
        :rtype: bool
        """
        character = self.get_character_by_id(character_id)

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
        """
        Sets the active character to the character associated with the given
        character ID. If the character ID is valid and corresponds to a character,
        the active character is updated, and the method returns True. Otherwise,
        the method returns False.

        :param character_id: The ID of the character to be set as active.
        :type character_id: Any
        :return: True if the active character was successfully updated, False if
                 the character ID is invalid or does not correspond to an existing
                 character.
        :rtype: bool
        """
        character = self.get_character_by_id(character_id)

        if character is None:
            return False

        self.active_character = character
        return True

    def get_active_character(self):
        """
        Retrieves the currently active character.

        This method is used to access the character that is currently active in the
        context of the object it is called on.

        :return: The currently active character instance.
        :rtype: Character
        """
        return self.active_character

    def get_default_character(self):
        """
        Retrieves the default character for the application.

        This method fetches the character instance associated with the default
        character ID defined in the `Character` class.

        :return: The default character instance.
        :rtype: Character
        """
        return self.get_character_by_id(Character.DEFAULT_CHARACTER_ID)

    def ensure_default_character(self, filename='data/characters.json'):
        """
        Ensures that a default character exists in the character list. If no default
        character is found, a new default character is created, configured with
        default presets, and added to the beginning of the character list. The
        updated list of characters is then saved to the specified file.

        :param filename: The file path where the character data is stored and
            will be saved. Defaults to 'data/characters.json'.
        :type filename: str
        :return: None
        """
        if self.get_default_character() is None:
            character = Character.create_default()
            character.load_default_presets()
            self.characters.insert(0, character)
            self.save_characters(filename)

if __name__ == "__main__":
    character_service = CharacterService()
    character_service.load_characters('C:\\Scripts\\Python\\dnd_dice_roller\\data\\characters.json')
    print(character_service.get_all_characters())