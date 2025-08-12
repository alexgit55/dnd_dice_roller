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
import random

import character
from skills_saves import SavingThrows, Skills

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
        _roll_check(self, check_type, combobox):
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
        self.frame_variable.set(3)  # Default to Skill Check
        self.advantage_var = tk.IntVar(self)
        self.advantage_var.set(0)  # Default to Normal
        self.frames={}
        self.create_widgets()
        self.show_frame() # Display the initial frame
        self.player_character = player_character

    def _roll_check(self, check_type, combobox):
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
        modifier = self.player_character.get_check_modifier(selected, check_type)
        if self.advantage_var.get() == 1:  # Advantage
            rolls = (random.randint(1, 20), random.randint(1, 20))
            roll = max(rolls)
        elif self.advantage_var.get() == 2:  # Disadvantage
            rolls = (random.randint(1, 20), random.randint(1, 20))
            roll = min(rolls)
        else:
            roll = random.randint(1, 20)
            rolls = (roll,)
        total = roll + modifier
        if modifier < 0:
            self.result_label.config(
                text=f"{selected}: {roll} - {abs(modifier)} = {total}")
        else:
            self.result_label.config(
                text=f"{selected}: {roll} + {modifier} = {total}")
    
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
            text="General Dice Roll", variable=self.frame_variable, value=2,
            command=self.show_frame).pack()
        tk.Radiobutton(
            top_frame, bg="lightblue",
            text="Skill Check", variable=self.frame_variable, value=3,
            command=self.show_frame).pack()
        tk.Radiobutton(
            top_frame, bg="lightblue",
            text="Saving Throw", variable=self.frame_variable, value=4,
            command=self.show_frame).pack()
        top_frame.pack()
        # Create a separator
        separator = tk.Frame(
            top_frame, height=2, bd=1, relief=tk.SUNKEN, bg="lightblue")
        separator.pack(fill=tk.X, padx=5, pady=5)
        #General Frame
        general_frame=tk.Frame(self, bg="lightblue")
        self.frames[2]=general_frame
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
        self.frames[3]=skill_check_frame
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
        skill_check_frame.pack()
        
        #Saving Throw Frame
        saving_throw_frame=tk.Frame(self, bg="lightblue")
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
        self.frames[4]=saving_throw_frame
        saving_throw_frame.pack()
        
        # Frame with radio buttons for advantage, disadvantage or normal
        # should appear just above the bottom frame
        advantage_disadvantage_frame = tk.Frame(self, bg="lightblue")
        self.frames[5] = advantage_disadvantage_frame
        separator = tk.Frame(
            advantage_disadvantage_frame, height=2, bd=1, relief=tk.SUNKEN, bg="lightblue")
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
        self.frames[1]=bottom_frame
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
        self.result_label=tk.Label(
            bottom_frame, bg="lightblue", text="", font=("Arial", 12))
        self.result_label.pack()
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
        if frame==3:
            self.frames[2].pack_forget()
            self.frames[4].pack_forget()
            self.frames[3].pack(before=self.frames[5])
        elif frame==4:
            self.frames[2].pack_forget()
            self.frames[3].pack_forget()
            self.frames[4].pack(before=self.frames[5])
        else:
            self.frames[3].pack_forget()
            self.frames[4].pack_forget()
            self.frames[2].pack(before=self.frames[5])

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
            Calls the _roll_check method for a skill check using the selected 
            skill.

        - For frame 4 (Saving Throw): 
            Calls the _roll_check method for a saving throw using the selected 
            saving throw.

        Assumes the presence of UI elements such as frames, spinboxes, option 
        menus, and result label.
        """
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
                self.result_label.config(
                    text=f"Rolls: {rolls} - {abs(dice_modifier)}, Total: {result}")
            elif dice_modifier > 0:
                self.result_label.config(
                    text=f"Rolls: {rolls} + {dice_modifier}, Total: {result}")
            else:
                self.result_label.config(text=f"Rolls: {rolls}, Total: {result}")
        if frame == 3:  # Skill Check
            self._roll_check("skill", self.skill_combobox)
        if frame == 4:  # Saving Throw
            self._roll_check("save", self.saving_throw_combobox)

if __name__ == "__main__":
    Warryn = character.Character(name="Warryn", proficiency_bonus=4)
    Warryn.set_save_proficiencies(["Strength", "Constitution"])
    Warryn.set_skill_proficiencies(
        ["Animal Handling", "Athletics", "Intimidation", "Perception", "Survival"])
    Warryn.set_skill_advantages(["Deception","Sleight of Hand"])
    Warryn.set_skill_disadvantages(["Stealth"])
    Warryn.set_save_advantages(["Intelligence","Wisdom","Charisma"])
    Warryn.set_ability_score("Strength", 19)
    Warryn.set_ability_score("Dexterity", 14)
    Warryn.set_ability_score("Constitution", 18)
    Warryn.set_ability_score("Intelligence", 9)
    Warryn.set_ability_score("Wisdom", 12)
    Warryn.set_ability_score("Charisma", 10)
    app = DiceRollerApp(player_character=Warryn)
    app.mainloop()