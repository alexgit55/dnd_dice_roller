import json
from domain.models.roll import Roll

class PresetRepository:

    @staticmethod
    def save_presets_to_file(preset_list, filename='data/presets.json'):

        data_to_write = [Roll.encode_roll(roll) for roll in preset_list if roll.roll_type == 'custom']
        with open(f'{filename}', 'w', encoding='utf-8') as f:
            json.dump(data_to_write, f, indent=4)

    @staticmethod
    def load_presets_from_file(filename='data/presets.json'):

        with open(f'{filename}', 'r', encoding='utf-8') as f:
            presets_json = f.read()
        presets_from_file = json.loads(presets_json)
        return [Roll.decode_roll(roll) for roll in presets_from_file]
