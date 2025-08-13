"""
dice_roller_main.py
A Tkinter-based GUI application for rolling dice in Dungeons & Dragons (D&D) 
games. This module defines the DiceRollerApp class, which provides an 
interactive interface for players to perform general dice rolls, skill checks, 
and saving throws, supporting advantage/disadvantage mechanics and modifiers. 
It is designed to work with a PlayerCharacter object that supplies skill and 
saving throw data.
Classes:
    DiceRollerApp (tk.Tk): 
        Main application window for the D&D Dice Roller, allowing users to 
        select roll types, input modifiers, and view results.
Functions:
    None (all logic is encapsulated within the DiceRollerApp class).
Example:
        # ... set up character ...
"""

import tkinter as tk
from tkinter import ttk

import character
from weapons import Weapon
from skills_saves import SavingThrows, Skills
from dice import Dice, DiceRoller
from messages import Messages

class DiceRollerApp(tk.Tk):
    """A Tkinter-based GUI application for rolling dice in Dungeons & Dragons 
    (D&D) games.The DiceRollerApp provides an interactive interface for players 
    to perform general dice rolls, skill checks, and saving throws, supporting
    advantage/disadvantage mechanics and modifiers. It is designed to work with 
    a PlayerCharacter object that supplies skill and saving throw data.
    Attributes:
        player_character: 
            The PlayerCharacter instance representing the current player.
        frame_variable (tk.IntVar): 
            Tracks which roll type frame is currently selected.
        advantage_var (tk.IntVar): 
            Tracks the advantage/disadvantage/normal state.
        frames (dict): 
            Stores references to the main UI frames.
        skill_combobox (tk.ttk.Combobox): 
            Dropdown for selecting skills.
        saving_throw_combobox (tk.ttk.Combobox): Dropdown for selecting saving 
            throws.
        result_label (tk.Label): Displays the result of the most recent roll.
    Methods:
        __init__(self, player_character):
            Initializes the application window, sets up variables, and builds 
            the UI.
        d20_check(self, check_type, combobox):
            Performs a skill check or saving throw roll, applying 
            advantage/disadvantage and modifiers, and updates the result label.
        create_widgets(self):
            Constructs and packs all UI widgets, including frames, buttons, 
            labels, and input controls.
        show_frame(self):
            Displays the appropriate frame based on the selected roll type.
        reset_values(self):
            Resets all input fields to their default values.
        update_advantage_disadvantage(self, check_type="skill", event=None):
            Updates the advantage/disadvantage state based on the selected 
            skill or saving throw.
        roll_dice(self):
            Handles the logic for rolling dice based on the selected frame 
            (general, skill, or save),
            retrieves input values, performs the roll(s), and updates the 
            result label.
    """
    
    def __init__(self, player_character):
        super().__init__()
        self.title("D&D Dice Roller")
        self.config(bg="lightblue")  # Add this line
        self.frame_variable=tk.IntVar(self)
        self.frame_variable.set(3)  # Default to General Dice Roll
        self.advantage_var = tk.IntVar(self)
        self.advantage_var.set(0)  # Default to Normal
        self.frames={}
        self.create_widgets()
        self.show_frame() # Display the initial frame
        self.player_character = player_character
        self.dice = DiceRoller()

    def clear_labels(self):
        self.advantage_label.config(text="")
        self.crit_label.config(text="")
        self.result_label.config(text="")
        self.attack_damage_label.config(text="")

    # Helper for updating advantage label
    def update_advantage_label(self, advantage, rolls):
        if advantage == 1:
            self.advantage_label.config(text=f"Advantage Roll: {rolls[0][0]} vs {rolls[0][1]} = {rolls[1]}")
        elif advantage == 2:
            self.advantage_label.config(text=f"Disadvantage Roll: {rolls[0][0]} vs {rolls[0][1]} = {rolls[1]}")
        else:
            self.advantage_label.config(text="")

    def update_crit_label(self, dice_roll):
        self.crit_label.config(text=f"{Messages.result_message(dice_roll)}")

    def update_result_label(self, combobox, dice_roll, modifier):      
        total = dice_roll + modifier
        if modifier < 0:
            self.result_label.config(
                text=f"{combobox}: {dice_roll} - {abs(modifier)} = {total}")
        else:
            self.result_label.config(
                text=f"{combobox}: {dice_roll} + {modifier} = {total}")

    def update_attack_damage_label(
        self,
        weapon_name,
        damage_rolls,
        damage_bonuses,
        total_damage
    ):
        self.attack_damage_label.config(
                text=f"{weapon_name} Damage: {damage_rolls} + {damage_bonuses} = {total_damage}")
    
    
    def roll_d20_with_advantage(self, advantage):
        rolls = self.dice.d20_roll(advantage=advantage)
        return rolls
    
    def general_roll(self):
        dice_type = int(self.frames[3].children['!optionmenu'].cget('text')[1:])
        number_of_dice = int(self.frames[3].children['!spinbox'].get())
        dice_modifier = int(self.frames[3].children['!spinbox2'].get())
        self.dice.clear_dice()
        if dice_type == 20 and number_of_dice == 1:
            advantage = self.advantage_var.get()
            rolls = self.roll_d20_with_advantage(advantage)
            self.update_advantage_label(advantage, rolls)
            roll=rolls[1]
            self.update_crit_label(roll)
            self.update_result_label("General Roll", roll, dice_modifier)
        else:
            for _ in range(number_of_dice):
                die = Dice(dice_type)
                self.dice.add_dice(die)
            total = self.dice.total_roll()
            self.update_result_label("General Roll", total, dice_modifier)

    def calculate_attack_damage(self, weapon_name, dice_roll, dice_modifier):
        attack_min=1
        weapon_modifier = dice_modifier - self.player_character.proficiency_bonus
        weapon = next((w for w in self.player_character.weapons if w.name == weapon_name), None)
        if weapon:
            if weapon.weight_type == "Heavy":
                attack_min=3
                self.player_character.damage_bonus = 4
            else:
                self.player_character.damage_bonus = 0
            num_dice = int(weapon.damage.split('d')[0])
            die_type = int(weapon.damage.split('d')[1])
            if dice_roll==20:
                num_dice *= 2
            self.dice.clear_dice()
            for _ in range(num_dice):
                self.dice.add_dice(Dice(die_type, min_roll=attack_min))
            damage_rolls = self.dice.roll_all()
            damage_bonuses=weapon_modifier+self.player_character.damage_bonus
            total_damage = sum(damage_rolls) + damage_bonuses
            self.update_attack_damage_label(
                weapon.name,
                damage_rolls,
                damage_bonuses,
                total_damage
            )
    
    def d20_check(self, check_type, combobox):
        """
        Rolls a d20 check for the selected ability or skill, applying advantage 
        or disadvantage if specified,and updates the result label with the roll 
        breakdown and total.

        Args:
            check_type (str): The type of check being performed (e.g., 
            'ability', 'skill'). 
            combobox (tkinter.ttk.Combobox): 
                The combobox widget containing the selectable abilities or 
                skills.

        Behavior:
            - Retrieves the selected ability or skill from the combobox.
            - Gets the corresponding modifier from the player character.
            - Rolls a d20, applying advantage (highest of two rolls) or 
                disadvantage (lowest of two rolls) if set.
            - Calculates the total by adding the modifier to the roll.
            - Updates the result label to display the roll, modifier, and total 
                in a formatted string.
        """
        selected = combobox.get()
        modifier = self.player_character.get_check_modifier(
            selected, check_type)
        advantage = self.advantage_var.get()
        rolls = self.roll_d20_with_advantage(advantage)
        self.update_advantage_label(advantage, rolls)

        roll=rolls[1]
        self.update_crit_label(roll)
        self.update_result_label(selected, roll, modifier)
            
        if check_type == "attack":
            self.calculate_attack_damage(
                selected,
                roll,
                modifier
            )

    def create_widgets(self):
        """
        Creates and arranges all the widgets for the dice roller application's 
        main window.
        This method sets up the following UI components using Tkinter:
            - Top frame with radio buttons to select the type of roll 
              (General Dice Roll, Skill Check, Saving Throw).
            - Separator for visual separation.
            - General frame for selecting dice type, number of dice, and 
              modifier.
            - Skill check frame with a combobox for skill selection and event 
              binding.
            - Saving throw frame with a combobox for saving throw selection and 
              event binding.
            - Advantage/disadvantage frame with radio buttons to select roll 
              mode (Normal, Advantage, Disadvantage).
            - Bottom frame with Roll and Reset buttons, a separator, and a 
              label to display results.
        Frames are stored in self.frames for easy access and management.
        Event bindings are set up for skill and saving throw selection to update 
        advantage/disadvantage options.
        """
        #Top Frame
        top_frame=tk.Frame(self, bg="lightblue")
        self.frames[0]=top_frame
        top_frame.pack(fill=tk.X)
        dice_roll_type=tk.Label(
            top_frame, bg="lightblue",
            text="Select which dtype of roll you want to perform: ")
        dice_roll_type.pack(pady=20)
        tk.Radiobutton(
            top_frame, bg="lightblue",
            text="General Dice Roll", variable=self.frame_variable, value=3,
            command=self.show_frame).pack()
        tk.Radiobutton(
            top_frame, bg="lightblue",
            text="Skill Check", variable=self.frame_variable, value=4,
            command=self.show_frame).pack()
        tk.Radiobutton(
            top_frame, bg="lightblue",
            text="Saving Throw", variable=self.frame_variable, value=5,
            command=self.show_frame).pack()
        tk.Radiobutton(
            top_frame, bg="lightblue",
            text="Weapon Attack", variable=self.frame_variable, value=6,
            command=self.show_frame).pack()
        top_frame.pack()
        # Create a separator
        separator = tk.Frame(
            top_frame, height=2, bd=1, relief=tk.SUNKEN, bg="lightblue")
        separator.pack(fill=tk.X, padx=5, pady=5)
        #General Frame
        general_frame=tk.Frame(self, bg="lightblue")
        self.frames[3]=general_frame
        dice_type=tk.StringVar(general_frame)
        dice_type.set("d20")  # Default value
        dice_type_label=tk.Label(
            general_frame, bg="lightblue",
            text="Select the dtype of Dice to Roll:")
        dice_type_label.pack()
        dice_type_menu=tk.OptionMenu(
            general_frame,
            dice_type, "d4", "d6", "d8", "d10", "d12", "d20"
        )
        dice_type_menu.config(bg="lightblue")
        dice_type_menu.pack()
        number_of_dice_label=tk.Label(
            general_frame, bg="lightblue", text="How many Dice to Roll?")
        number_of_dice_label.pack()
        number_of_dice=tk.Spinbox(
            general_frame, bg="lightblue", from_=1, to=20, width=5)
        number_of_dice.pack()
        dice_modifier_label=tk.Label(
            general_frame, bg="lightblue", text="Modifier to add to the roll?")
        dice_modifier_label.pack()
        dice_modifier=tk.Spinbox(
            general_frame, bg="lightblue", from_=-20, to=20, width=5,
            textvariable=tk.IntVar(general_frame, value=0))
        dice_modifier.pack()
        general_frame.pack(fill=tk.X, pady=10)
        
        # Skill Check Frame
        skill_check_frame=tk.Frame(self, bg="lightblue")
        self.frames[4]=skill_check_frame
        skill_check_label=tk.Label(
            skill_check_frame, bg="lightblue", text="Which Skill check to roll?")
        skill_check_label.pack()
        # Combobox for skill selection
        self.skill_combobox = tk.ttk.Combobox(
            skill_check_frame, values=list(Skills.ability_map.keys()))
        # Change advantage/disadvantage based on selection
        self.skill_combobox.bind(
            "<<ComboboxSelected>>", lambda event: 
                self.update_advantage_disadvantage("skill", event))
        self.skill_combobox.pack()
        skill_check_frame.pack(fill=tk.X, pady=10)
        
        #Saving Throw Frame
        saving_throw_frame=tk.Frame(self, bg="lightblue")
        self.frames[5]=saving_throw_frame
        saving_throw_label=tk.Label(
            saving_throw_frame, bg="lightblue",
            text="Which Saving Throw to Roll?")
        saving_throw_label.pack()
        # Combobox for saving throw selection
        self.saving_throw_combobox = tk.ttk.Combobox(
            saving_throw_frame, values=list(SavingThrows.ability_map.keys()))
        self.saving_throw_combobox.bind(
            "<<ComboboxSelected>>", lambda event: 
                self.update_advantage_disadvantage("save", event))
        self.saving_throw_combobox.pack()
        saving_throw_frame.pack(fill=tk.X, pady=10)
        
        # Weapon attack frame
        weapon_attack_frame = tk.Frame(self, bg="lightblue")
        self.frames[6] = weapon_attack_frame
        separator = tk.Frame(
            weapon_attack_frame, height=2,
            bd=1, relief=tk.SUNKEN, bg="lightblue")
        separator.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(weapon_attack_frame, bg="lightblue", text="Select Weapon:").pack()
        self.weapon_combobox = tk.ttk.Combobox(
            weapon_attack_frame, values=[weapon.name for weapon in Warryn.weapons])
        self.weapon_combobox.pack()
        weapon_attack_frame.pack(fill=tk.X, pady=10)

        # Frame with radio buttons for advantage, disadvantage or normal
        # should appear just above the bottom frame
        advantage_disadvantage_frame = tk.Frame(self, bg="lightblue")
        self.frames[1] = advantage_disadvantage_frame
        separator = tk.Frame(
            advantage_disadvantage_frame, height=2, 
            bd=1, relief=tk.SUNKEN, bg="lightblue")
        separator.pack(fill=tk.X, padx=5, pady=5)
        tk.Radiobutton(
            advantage_disadvantage_frame, text="Normal", 
            variable=self.advantage_var, value=0, 
            bg="lightblue").pack(side=tk.LEFT)
        tk.Radiobutton(
            advantage_disadvantage_frame, text="Advantage", 
            variable=self.advantage_var, value=1, 
            bg="lightblue").pack(side=tk.LEFT)
        tk.Radiobutton(
            advantage_disadvantage_frame, text="Disadvantage", 
            variable=self.advantage_var, value=2, 
            bg="lightblue").pack(side=tk.LEFT)
        advantage_disadvantage_frame.pack()

        # Bottom Roll Frame
        bottom_frame=tk.Frame(self, bg="lightblue")
        self.frames[2]=bottom_frame
        # Create a separator
        separator = tk.Frame(
            bottom_frame, height=2, bd=1, relief=tk.SUNKEN, bg="lightblue")
        separator.pack(fill=tk.X, padx=5, pady=5)
        roll_button=tk.Button(
            bottom_frame, text="Roll Dice", command=self.roll_dice)
        roll_button.pack(pady=20)
        reset_button=tk.Button(
            bottom_frame, text="Reset", command=self.reset_values)
        reset_button.pack(pady=5)
        self.advantage_label = tk.Label(
            bottom_frame, bg="lightblue", text="", font=("Arial", 12))
        self.advantage_label.pack()
        self.result_label=tk.Label(
            bottom_frame, bg="lightblue", text="", font=("Arial", 12))
        self.result_label.pack()
        self.crit_label = tk.Label(
            bottom_frame, bg="lightblue", text="", font=("Arial", 12))
        self.crit_label.pack()
        self.attack_damage_label = tk.Label(
            bottom_frame, bg="lightblue", text="", font=("Arial", 12))
        self.attack_damage_label.pack()
        bottom_frame.pack(fill=tk.X, pady=10)
    
    def show_frame(self):
        """
        Displays the appropriate frame in the GUI based on the current value of 
        `self.frame_variable`.

        This method manages the visibility and order of frames in the 
        application by packing or forgetting specific frames. It ensures that 
        only the selected frame (2, 3, or 4) is visible before frame 5, while 
        hiding the others.

        Behavior:
            - If `frame_variable` is 3: Shows frame 3, hides frames 2 and 4.
            - If `frame_variable` is 4: Shows frame 4, hides frames 2 and 3.
            - Otherwise: Shows frame 2, hides frames 3 and 4.
        """
        frame=self.frame_variable.get()
        if frame==4:
            self.frames[3].pack_forget()
            self.frames[5].pack_forget()
            self.frames[6].pack_forget()
            self.frames[4].pack(before=self.frames[2])
        elif frame==5:
            self.frames[3].pack_forget()
            self.frames[4].pack_forget()
            self.frames[6].pack_forget()
            self.frames[5].pack(before=self.frames[2])
        elif frame==6:
            self.frames[3].pack_forget()
            self.frames[4].pack_forget()
            self.frames[5].pack_forget()
            self.frames[6].pack(before=self.frames[2])
        else:
            self.frames[4].pack_forget()
            self.frames[5].pack_forget()
            self.frames[6].pack_forget()
            self.frames[3].pack(before=self.frames[2])

    def reset_values(self):
        """Set default values for all inputs."""
        pass

    def update_advantage_disadvantage(self, check_type="skill", event=None):
        """
        Updates the advantage/disadvantage state for the selected skill or 
        saving throw.

        Depending on the `check_type`, this method checks if the currently 
        selected skill or saving throw has advantage, disadvantage, or neither 
        for the player character, and updates the `advantage_var`
        accordingly:
            - 1: Advantage
            - 2: Disadvantage
            - 0: Neither

        Args:
            check_type (str): Type of check to update ("skill" or "save"). 
                Defaults to "skill".
            event (Optional[Any]): Optional event parameter for use with event 
            bindings. Defaults to None.
        """
        if check_type == "skill":
            selected = self.skill_combobox.get()
            if self.player_character.skills.has_advantage(selected):
                self.advantage_var.set(1)
            elif self.player_character.skills.has_disadvantage(selected):
                self.advantage_var.set(2)
            else:
                self.advantage_var.set(0)
        elif check_type == "save":
            selected = self.saving_throw_combobox.get()
            if self.player_character.saving_throws.has_advantage(selected):
                self.advantage_var.set(1)
            elif self.player_character.saving_throws.has_disadvantage(selected):
                self.advantage_var.set(2)
            else:
                self.advantage_var.set(0)

    def roll_dice(self):
        """
        Handles dice rolling logic based on the currently selected frame.

        - For frame 2 (General Dice Roll): 
            Retrieves the selected dice type, number of dice, and modifier from 
            the UI, performs the dice rolls, applies the modifier, and updates 
            the result label with the individual rolls and the total.

        - For frame 3 (Skill Check): 
            Calls the d20_check method for a skill check using the selected 
            skill.

        - For frame 4 (Saving Throw): 
            Calls the d20_check method for a saving throw using the selected 
            saving throw.

        Assumes the presence of UI elements such as frames, spinboxes, option 
        menus, and result label.
        """
        self.clear_labels()  # Clear all labels before rolling
        frame = self.frame_variable.get()
        if frame == 4:  # Skill Check
            self.d20_check("skill", self.skill_combobox)
        elif frame == 5:  # Saving Throw
            self.d20_check("save", self.saving_throw_combobox)
        elif frame == 6:  # Weapon Attack
            self.d20_check("attack", self.weapon_combobox)
        else:  # General Dice Roll
            self.general_roll()
        

if __name__ == "__main__":
    Warryn = character.Character(name="Warryn", proficiency_bonus=4)
    Warryn.saving_throws.set_proficiencies(["Strength", "Constitution"])
    Warryn.skills.set_proficiencies([
        "Animal Handling", "Athletics", "Intimidation", "Perception", "Survival"])
    Warryn.skills.set_advantages(["Deception","Sleight of Hand"])
    Warryn.skills.set_disadvantages(["Stealth"])
    Warryn.saving_throws.set_advantages(["Intelligence","Wisdom","Charisma"])
    Warryn.set_ability_score("Strength", 19)
    Warryn.set_ability_score("Dexterity", 14)
    Warryn.set_ability_score("Constitution", 18)
    Warryn.set_ability_score("Intelligence", 9)
    Warryn.set_ability_score("Wisdom", 12)
    Warryn.set_ability_score("Charisma", 10)
    Warryn.add_weapon(Weapon("Glaive", "martial", "slashing", "1d10", weight_type="Heavy"))
    Warryn.add_weapon(Weapon("Maul", "martial", "bludgeoning", "2d6", weight_type="Heavy"))
    app = DiceRollerApp(player_character=Warryn)
    app.mainloop()