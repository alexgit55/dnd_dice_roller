"""Character class for the dice roller application"""
# This class will save character information and manage dice rolls

from skills_saves import SavingThrows, Skills


class Character:
    def __init__(self, name, ability_scores=None, proficiency_bonus=2):
        self.name = name
        self.ability_scores = ability_scores if ability_scores else {}
        self.proficiency_bonus = proficiency_bonus
        self.skills = Skills()
        self.saving_throws = SavingThrows()

    def set_ability_score(self, ability, score):
        """Set an ability score for the character."""
        self.ability_scores[ability] = score
        
    def get_ability_score(self, ability):
        """Get an ability score for the character."""
        return self.ability_scores.get(ability, 0)
    
    def calculate_ability_modifier(self, ability):
        """Calculate the modifier for an ability score."""
        score = self.get_ability_score(ability)
        return (score - 10) // 2
        
    def set_save_proficiencies(self, proficiencies):
        """Set save proficiencies for the character."""
        self.saving_throws.set_proficiencies(proficiencies)

    def set_skill_proficiencies(self, proficiencies):
        """Set skill proficiencies for the character."""
        self.skills.set_proficiencies(proficiencies)
        
    def set_skill_advantages(self, advantages):
        """Set skill advantages for the character."""
        self.skills.set_advantages(advantages)

    def set_skill_disadvantages(self, disadvantages):
        """Set skill disadvantages for the character."""
        self.skills.set_disadvantages(disadvantages)
        
    def set_save_advantages(self, advantages):
        """Set save advantages for the character."""
        self.saving_throws.set_advantages(advantages)
        
    def set_save_disadvantages(self, disadvantages):
        """Set save disadvantages for the character."""
        self.saving_throws.set_disadvantages(disadvantages)

    def get_check_modifier(self, check, check_type="skill"):
        """
        Get the modifier for a skill or saving throw.
        check: Name of the skill or saving throw.
        check_type: "skill" or "save".
        """
        if check_type == "skill":
            ability = self.skills.ability_map.get(check)
            is_proficient = self.skills.is_proficient(check)
        elif check_type == "save":
            ability = self.saving_throws.ability_map.get(check)
            is_proficient = self.saving_throws.is_proficient(check)
        else:
            raise ValueError("check_type must be 'skill' or 'save'")

        modifier = self.calculate_ability_modifier(ability)

        if is_proficient:
            modifier += self.proficiency_bonus

        return modifier


John = Character(name="John", proficiency_bonus=5)
John.set_save_proficiencies(["Strength", "Constitution"])
John.set_skill_proficiencies(
    ["Animal Handling", "Athletics", "Intimidation", "Perception", "Survival"])
John.set_ability_score("Strength", 20)
John.set_ability_score("Dexterity", 14)
John.set_ability_score("Constitution", 15)
John.set_ability_score("Intelligence", 12)
John.set_ability_score("Wisdom", 13)
John.set_ability_score("Charisma", 10)

# Example usage
if __name__ == "__main__":
    print(f"Character Name: {John.name}")
    print(f"Strength Modifier: {John.calculate_ability_modifier('Strength')}")
    print(f"Proficiency Bonus: {John.proficiency_bonus}")
