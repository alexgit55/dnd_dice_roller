"""Classes representing Skills and Saving Throws"""


class Skills:
    skill_ability_map = {
        "Acrobatics": "Dexterity",
        "Animal Handling": "Wisdom",
        "Arcana": "Intelligence",
        "Athletics": "Strength",
        "Deception": "Charisma",
        "History": "Intelligence",
        "Insight": "Wisdom",
        "Intimidation": "Charisma",
        "Investigation": "Intelligence",
        "Medicine": "Wisdom",
        "Nature": "Intelligence",
        "Perception": "Wisdom",
        "Performance": "Charisma",
        "Persuasion": "Charisma",
        "Religion": "Intelligence",
        "Sleight of Hand": "Dexterity",
        "Stealth": "Dexterity",
        "Survival": "Wisdom"       
    }

    def __init__(self):
        self.proficiencies = []
        self.advantages = []
        self.disadvantages = []

    def set_proficiencies(self, proficiencies):
        self.proficiencies = proficiencies
        
    def set_advantages(self, advantages):
        """Set skill advantages for the character."""
        self.advantages = advantages

    def set_disadvantages(self, disadvantages):
        """Set skill disadvantages for the character."""
        self.disadvantages = disadvantages

    def is_proficient(self, skill):
        return skill in self.proficiencies

    def has_advantage(self, skill):
        return skill in self.advantages

    def has_disadvantage(self, skill):
        return skill in self.disadvantages

class SavingThrows:
    def __init__(self):
        self.saving_throws = {}
        self.proficiencies = []

    def set_saving_throw(self, save, value):
        self.saving_throws[save] = value

    def get_saving_throw(self, save):
        return self.saving_throws.get(save, 0)

    def set_proficiencies(self, proficiencies):
        self.proficiencies = proficiencies

    def is_proficient(self, save):
        return save in self.proficiencies