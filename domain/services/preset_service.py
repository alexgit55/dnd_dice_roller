import json
from domain.roll import Roll

class PresetService:
    def __init__(self):
        self.presets = []

    def add_preset(self, roll):
        self.presets.append(roll)

    def get_presets_by_type(self, roll_type=None):
        if roll_type is None:
            return self.presets
        else:
            return [preset for preset in self.presets if preset.roll_type == roll_type]

    def get_presets_by_character(self, character_id):
        return [preset for preset in self.presets if preset.character_id == character_id]

    def add_character_default_presets(self, character):
        for preset in character.default_presets.rolls:
            self.presets.append(preset)

    def get_preset(self, index):
        try:
            return self.presets[index]
        except IndexError:
            raise IndexError("Roll index out of range")

    def get_preset_index(self, roll):
        return self.presets.index(roll)

    def update_preset(self, roll, index):
        self.presets[index] = roll

    def remove_preset(self, index):
        del self.presets[index]

    def clear_presets(self):
        self.presets.clear()

    def save_to_file(self, filename='data/presets.json'):
        """
        Saves the current rolls data to a specified JSON file. The rolls are
        encoded using the `encode_roll` method of the `Roll` class, and the
        result is written to the file in a readable JSON format.

        :param filename: Name of the file where the data will be saved. The
            file will be created or overwritten if it already exists.
        :type filename: str
        :return: None
        """
        data_to_write = [Roll.encode_roll(roll) for roll in self.presets if roll.roll_type == 'custom']
        with open(f'{filename}', 'w', encoding='utf-8') as f:
            json.dump(data_to_write, f, indent=4)

    def load_from_file(self, filename='data/presets.json'):
        """
        Loads roll data from a specified JSON file and populates the current instance with the
        deserialized roll information.

        :param filename: The name of the JSON file to read and load roll data from.
        :type filename: str
        :return: None
        """
        self.clear_presets()
        with open(f'{filename}', 'r', encoding='utf-8') as f:
            presets_json = f.read()
        presets_list = json.loads(presets_json)
        self.presets = [Roll.decode_roll(roll) for roll in presets_list]