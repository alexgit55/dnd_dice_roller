# Character class for the dice roller application
# This class will save character information and manage dice rolls

class Character:
    def __init__(self, name, ability_scores=None, proficiency_bonus=2):
        self.name = name
        self.ability_scores = ability_scores if ability_scores else {}
        self.proficiency_bonus = proficiency_bonus
        
    def set_ability_score(self, ability, score):
        """Set an ability score for the character."""
        self.ability_scores[ability] = score
        
    def get_ability_score(self, ability):
        """Get an ability score for the character."""
        return self.ability_scores.get(ability, 0)
    
    def calculate_modifier(self, ability):
        """Calculate the modifier for an ability score."""
        score = self.get_ability_score(ability)
        return (score - 10) // 2
        
    def set_save_proficiencies(self, proficiencies):
        """Set save proficiencies for the character."""
        self.save_proficiencies = proficiencies
        
    def set_skill_proficiencies(self, proficiencies):
        """Set skill proficiencies for the character."""
        self.skill_proficiencies = proficiencies



John = Character(name="John", proficiency_bonus=5)
John.set_save_proficiencies(["Strength", "Constitution"])
John.set_skill_proficiencies(["Animal Handling", "Athletics", "Intimidation", "Perception", "Survival"])
John.set_ability_score("Strength", 20)
John.set_ability_score("Dexterity", 14)
John.set_ability_score("Constitution", 15)
John.set_ability_score("Intelligence", 12)
John.set_ability_score("Wisdom", 13)
John.set_ability_score("Charisma", 10)

# Example usage
if __name__ == "__main__":
    print(f"Character Name: {John.name}")
    print(f"Strength Modifier: {John.calculate_modifier('Strength')}")
    print(f"Proficiency Bonus: {John.proficiency_bonus}")
    