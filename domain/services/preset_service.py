from storage.preset_repository import PresetRepository

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

    def save_presets(self, filename='data/presets.json'):
        PresetRepository.save_presets_to_file(self.presets, filename)

    def load_presets(self, filename='data/presets.json'):
       self.presets = PresetRepository.load_presets_from_file(filename)