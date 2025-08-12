"""Classes representing Skills and Saving Throws"""

class Checks:
    ability_map={}
    
    def __init__(self):
        self.proficiencies = []
        self.advantages = []
        self.disadvantages = []
    
    def set_proficiencies(self, proficiencies):
        self.proficiencies = proficiencies
    
    def set_advantages(self, advantages):
        self.advantages = advantages

    def set_disadvantages(self, disadvantages):
        self.disadvantages = disadvantages
        
    def is_proficient(self, check):
        return check in self.proficiencies
    
    def has_advantage(self, check):
        return check in self.advantages

    def has_disadvantage(self, check):
        return check in self.disadvantages

class Skills(Checks):
    ability_map = {
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

class SavingThrows(Checks):
    ability_map = {
        "Strength": "Strength",
        "Dexterity": "Dexterity",
        "Constitution": "Constitution",
        "Intelligence": "Intelligence",
        "Wisdom": "Wisdom",
        "Charisma": "Charisma"
    }