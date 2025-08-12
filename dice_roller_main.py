import tkinter as tk
from tkinter import ttk
import random

import character
from skills_saves import SavingThrows, Skills

class DiceRollerApp(tk.Tk):
    def __init__(self, player_character):
        super().__init__()
        self.title("D&D Dice Roller")
        self.config(bg="lightblue")  # Add this line
        self.frame_variable=tk.IntVar(self)
        self.frame_variable.set(3)  # Default to Skill Check
        self.frames={}
        self.create_widgets()
        self.show_frame() # Display the initial frame
        self.player_character = player_character

    def create_widgets(self):
        #Top Frame
        top_frame=tk.Frame(self, bg="lightblue")
        self.frames[0]=top_frame
        top_frame.pack(fill=tk.X)
        dice_roll_type=tk.Label(top_frame, bg="lightblue", text="Select which dtype of roll you want to perform: ")
        dice_roll_type.pack(pady=20)       
        tk.Radiobutton(top_frame, bg="lightblue", text="General Dice Roll", variable=self.frame_variable, value=2,
                   command=self.show_frame).pack()
        tk.Radiobutton(top_frame, bg="lightblue", text="Skill Check", variable=self.frame_variable, value=3,
                   command=self.show_frame).pack()
        tk.Radiobutton(top_frame, bg="lightblue", text="Saving Throw", variable=self.frame_variable, value=4,
                   command=self.show_frame).pack()
        top_frame.pack()
        
        # Create a separator
        separator = tk.Frame(top_frame, height=2, bd=1, relief=tk.SUNKEN, bg="lightblue")
        separator.pack(fill=tk.X, padx=5, pady=5)
        
        #General Frame
        general_frame=tk.Frame(self, bg="lightblue")
        self.frames[2]=general_frame
        dice_type=tk.StringVar(general_frame)
        dice_type.set("d20")  # Default value
        dice_type_label=tk.Label(general_frame, bg="lightblue", text="Select the dtype of Dice to Roll:")
        dice_type_label.pack()
        dice_type_menu=tk.OptionMenu(general_frame, dice_type, "d4", "d6", "d8", "d10", "d12", "d20")
        dice_type_menu.config(bg="lightblue")
        dice_type_menu.pack()
        number_of_dice_label=tk.Label(general_frame, bg="lightblue", text="How many Dice to Roll?")
        number_of_dice_label.pack()
        number_of_dice=tk.Spinbox(general_frame, bg="lightblue", from_=1, to=20, width=5)
        number_of_dice.pack()
        dice_modifier_label=tk.Label(general_frame, bg="lightblue", text="Modifier to add to the roll?")
        dice_modifier_label.pack()
        dice_modifier=tk.Spinbox(general_frame, bg="lightblue", from_=-20, to=20, width=5,textvariable=tk.IntVar(general_frame, value=0))
        dice_modifier.pack()
        general_frame.pack(fill=tk.X, pady=10)
        
        # Skill Check Frame
        skill_check_frame=tk.Frame(self, bg="lightblue")
        self.frames[3]=skill_check_frame
        skill_check_label=tk.Label(skill_check_frame, bg="lightblue", text="Which Skill check to roll?")
        skill_check_label.pack()
        # Combobox for skill selection
        self.skill_combobox = tk.ttk.Combobox(skill_check_frame, values=list(Skills.skill_ability_map.keys()))
        self.skill_combobox.pack()
        skill_check_frame.pack()
        
        #Saving Throw Frame
        saving_throw_frame=tk.Frame(self, bg="lightblue")
        saving_throw_label=tk.Label(saving_throw_frame, bg="lightblue", text="Which Saving Throw to Roll?")
        saving_throw_label.pack()
        self.frames[4]=saving_throw_frame
        saving_throw_frame.pack()
        
        # Bottom Roll Frame
        bottom_frame=tk.Frame(self, bg="lightblue")
        self.frames[1]=bottom_frame
        # Create a separator
        separator = tk.Frame(bottom_frame, height=2, bd=1, relief=tk.SUNKEN, bg="lightblue")
        separator.pack(fill=tk.X, padx=5, pady=5)
        roll_button=tk.Button(bottom_frame, text="Roll Dice", command=self.roll_dice)
        roll_button.pack(pady=20)
        reset_button=tk.Button(bottom_frame, text="Reset", command=self.reset_values)
        reset_button.pack(pady=5)
        self.result_label=tk.Label(bottom_frame, bg="lightblue", text="", font=("Arial", 12))
        self.result_label.pack()
        bottom_frame.pack(fill=tk.X, pady=10)
    
    def show_frame(self):
        frame=self.frame_variable.get()
        if frame==3:
            self.frames[2].pack_forget()
            self.frames[4].pack_forget()
            self.frames[3].pack(before=self.frames[1])
        elif frame==4:
            self.frames[2].pack_forget()
            self.frames[3].pack_forget()
            self.frames[4].pack(before=self.frames[1])
        else:
            self.frames[3].pack_forget()
            self.frames[4].pack_forget()
            self.frames[2].pack(before=self.frames[1])

    def reset_values(self):
        """Set default values for all inputs."""
        pass

    def roll_dice(self):
        frame = self.frame_variable.get()
        if frame == 2:  # General Dice Roll
            dice_type = self.frames[2].children['!optionmenu'].cget('text')
            number_of_dice = int(self.frames[2].children['!spinbox'].get())
            dice_modifier = int(self.frames[2].children['!spinbox2'].get())
            rolls=[]
            for _ in range(number_of_dice):
                dtype=int(dice_type[1:])
                roll=random.randint(1,dtype)
                rolls.append(roll)
            result=sum(rolls)+dice_modifier
            if dice_modifier < 0:
                self.result_label.config(text=f"Rolls: {rolls} - {abs(dice_modifier)}, Total: {result}")
            elif dice_modifier > 0:
                self.result_label.config(text=f"Rolls: {rolls} + {dice_modifier}, Total: {result}")
            else:
                self.result_label.config(text=f"Rolls: {rolls}, Total: {result}")
        if frame == 3:  # Skill Check
            selected_skill = self.skill_combobox.get()
            if (self.player_character.skills.has_advantage(selected_skill)):
                rolls = (random.randint(1, 20), random.randint(1, 20))
                roll = max(rolls)
            elif (self.player_character.skills.has_disadvantage(selected_skill)):
                rolls = (random.randint(1, 20), random.randint(1, 20))
                roll = min(rolls)
            else:
                roll = random.randint(1, 20)
                rolls = (roll,)
            if selected_skill and self.player_character:
                modifier = self.player_character.get_skill_modifier(selected_skill)
                total = roll + modifier
                if modifier < 0:
                    self.result_label.config(text=f"{selected_skill}: {roll} - {abs(modifier)} = {total}")
                else:
                    self.result_label.config(text=f"{selected_skill}: {roll} + {modifier} = {total}")

if __name__ == "__main__":
    John = character.Character(name="John", proficiency_bonus=4)
    John.set_save_proficiencies(["Strength", "Constitution"])
    John.set_skill_proficiencies(
        ["Animal Handling", "Athletics", "Intimidation", "Perception", "Survival"])
    John.set_skill_advantages(["Deception","Sleight of Hand"])
    John.set_skill_disadvantages(["Stealth"])
    John.set_ability_score("Strength", 19)
    John.set_ability_score("Dexterity", 14)
    John.set_ability_score("Constitution", 18)
    John.set_ability_score("Intelligence", 9)
    John.set_ability_score("Wisdom", 12)
    John.set_ability_score("Charisma", 10)
    app = DiceRollerApp(player_character=John)
    app.mainloop()
    