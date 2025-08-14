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

import ttkbootstrap as tb

import character
from weapons import Weapon
from skills_saves import SavingThrows, Skills
from dice import Dice, DiceRoller
from messages import Messages


class DiceRollerApp(tb.Window):
    """A Tkinter-based GUI application for rolling dice in Dungeons & Dragons 
    (D&D) gameplay. The DiceRollerApp provides an interactive interface for 
    players to perform various dice rolls, including general dice rolls, skill 
    checks, saving throws, and weapon attacks. It supports rolling with 
    advantage or disadvantage, applies character modifiers, and displays results
    in a user-friendly format.
    Features:
        - General dice rolling for any dice type and quantity.
        - Skill checks and saving throws with automatic modifier calculation.
        - Weapon attack rolls with damage calculation based on weapon properties.
        - Advantage/disadvantage mechanics for applicable rolls.
        - Dynamic UI components for selecting roll type, dice, modifiers, and 
          character abilities.
        - Result display including roll breakdown, critical hit indication, and 
          damage calculation.
        player_character: An object representing the player's character,
        containing relevant attributes such as skills, saving throws, weapons, 
        and proficiency bonus.
    Attributes:
        frame_variable (tk.IntVar): Tracks the currently selected roll type 
            frame.
        advantage_var (tk.IntVar): Tracks the advantage/disadvantage state for 
            rolls.
        frames (dict): Stores references to UI frames for easy management.
        dice (DiceRoller): Dice rolling logic handler.
        skill_combobox (ttk.Combobox): UI element for skill selection.
        saving_throw_combobox (ttk.Combobox): UI element for saving throw 
            selection.
        weapon_combobox (ttk.Combobox): UI element for weapon selection.
        advantage_label (tk.Label): Displays advantage/disadvantage roll 
            details.
        result_label (tk.Label): Displays the result of the roll.
        crit_label (tk.Label): Displays critical hit information.
        attack_damage_label (tk.Label): Displays weapon attack damage details.
    Methods:
        clear_labels(): Clears all result display labels.
        update_advantage_label(advantage, rolls): Updates the 
            advantage/disadvantage label.
        update_crit_label(dice_roll): Updates the critical hit label.
        update_result_label(combobox, dice_roll, modifier): Updates the result 
            label with roll breakdown.
        update_attack_damage_label(weapon_name, damage_rolls, damage_bonuses, 
            total_damage): Updates the attack damage label.
        roll_d20_with_advantage(advantage): Rolls a d20 with 
            advantage/disadvantage logic.
        general_roll(): Handles general dice rolling logic.
        calculate_attack_damage(weapon_name, dice_roll, dice_modifier): 
            Calculates and displays weapon attack damage.
        d20_check(check_type, combobox): Performs a d20 check for skills, saving 
            throws, or attacks.
        create_widgets(): Initializes and arranges all UI widgets and frames.
        show_frame(): Displays the appropriate frame based on selected roll 
            type.
        reset_values(): Resets all input fields to their default values.
        update_advantage_disadvantage(check_type="skill", event=None): Updates 
            advantage/disadvantage state based on selection.
        roll_dice(): Main handler for rolling dice based on current UI state.
    Usage:
        Instantiate DiceRollerApp with a player character object and call 
        mainloop() to start the GUI.
    """

    def __init__(self, player_character):
        super().__init__(themename="darkly")
        self.title("D&D Dice Roller")
        self.create_control_variables()
        self.frames = {}
        self.skill_combobox = None
        self.saving_throw_combobox = None
        self.weapon_combobox = None
        self.advantage_label = None
        self.result_label = None
        self.crit_label = None
        self.attack_damage_label = None
        self.player_character = player_character
        self.dice = DiceRoller()
        self.create_widgets()
        self.show_frame() # Display the initial frame

    def create_control_variables(self):
        """
        Initializes control variables for the dice roller application.

        This method sets up the following tkinter variables:
            - advantage_var (IntVar): Indicates advantage state (0 = Normal).
            - frame_variable (StringVar): Specifies the current frame ("general" by default).
            - dice_type (StringVar): Type of dice to roll ("d20" by default).
            - number_of_dice (IntVar): Number of dice to roll (default is 1).
            - dice_modifier (IntVar): Modifier to add to the dice roll (default is 0).
        """
        self.advantage_var = tb.IntVar(self)
        self.advantage_var.set(0)  # Default to Normal
        self.frame_variable = tb.StringVar(self)
        self.frame_variable.set("general")  # Default to General Frame
        self.dice_type = tb.StringVar(self)
        self.dice_type.set("d20")
        self.number_of_dice = tb.IntVar(self)
        self.number_of_dice.set(1)  # Default to 1
        self.dice_modifier = tb.IntVar(self)
        self.dice_modifier.set(0)  # Default to 0

    def create_widgets(self):
        """
        Creates and arranges all the widgets for the dice roller application's 
        main window. Refactored to use helper methods for each frame.
        """
        self.create_top_frame()
        self.create_general_frame()
        self.create_skill_check_frame()
        self.create_saving_throw_frame()
        self.create_weapon_attack_frame()
        self.create_advantage_disadvantage_frame()
        self.create_bottom_frame()

    def create_top_frame(self):
        """
        Creates the top frame of the application UI, containing radio buttons 
        for selecting the type of dice roll.
        
        The frame includes:
            - A label prompting the user to select the type of roll.
            - Four radio buttons for "General Dice Roll", "Skill Check", 
            "Saving Throw", and "Weapon Attack".
            - A separator line for visual separation.
        
        The selected radio button updates the frame variable and triggers the 
        display of the corresponding frame.
        """
        top_frame = tb.Frame(self)
        self.frames["top"] = top_frame
        top_frame.pack(fill=tb.X)
        dice_roll_type = tb.Label(
            top_frame,
            text="Select which type of roll you want to perform: ",
            bootstyle="info",
            font=("Arial", 12, "bold")
        )
        dice_roll_type.pack(pady=20)
        tb.Radiobutton(
            top_frame,
            text="General Dice Roll", variable=self.frame_variable, value="general",
            command=self.show_frame).pack(side=tb.LEFT, padx=5)
        tb.Radiobutton(
            top_frame,
            text="Skill Check", variable=self.frame_variable, value="skill",
            command=self.show_frame).pack(side=tb.LEFT, padx=5)
        tb.Radiobutton(
            top_frame,
            text="Saving Throw", variable=self.frame_variable, value="save",
            command=self.show_frame).pack(side=tb.LEFT, padx=5)
        tb.Radiobutton(
            top_frame,
            text="Weapon Attack", variable=self.frame_variable, value="weapon",
            command=self.show_frame).pack(side=tb.LEFT, padx=5)

    def create_advantage_disadvantage_frame(self):
        """
        Creates and packs a frame containing radio buttons for selecting dice 
        roll mode: Normal, Advantage, or Disadvantage. The selected mode is 
        stored in self.advantage_var. The frame is stored in self.frames["advantage"] and 
        styled with a light blue background.
        """
        advantage_disadvantage_frame = tb.Frame(
            self,
            padding=(10, 5, 10, 5)
            )
        self.frames["advantage"] = advantage_disadvantage_frame
        tb.Label(
            advantage_disadvantage_frame, text="Roll Mode:",
            bootstyle="info",
            font=("Arial", 12, "bold")
            ).pack(side=tb.TOP, padx=5)
        tb.Radiobutton(
            advantage_disadvantage_frame, text="Normal",
            variable=self.advantage_var, value=0,
            style="Advantage.TRadiobutton",
            padding=(10, 5, 10, 5)
        ).pack(side=tb.LEFT, padx=20)
        tb.Radiobutton(
            advantage_disadvantage_frame, text="Advantage",
            variable=self.advantage_var, value=1,
            style="Advantage.TRadiobutton",
            padding=(10, 5, 10, 5)
        ).pack(side=tb.LEFT, padx=5)
        tb.Radiobutton(
            advantage_disadvantage_frame, text="Disadvantage",
            variable=self.advantage_var, value=2,
            style="Advantage.TRadiobutton",
            padding=(10, 5, 10, 5)
        ).pack(side=tb.LEFT, padx=5)
        advantage_disadvantage_frame.pack(fill=tb.X, pady=10)

    def create_general_frame(self):
        """
        Creates and configures the general frame for dice rolling options in 
        the GUI.

        This frame allows the user to:
            - Select the type of dice to roll (d4, d6, d8, d10, d12, d20).
            - Specify the number of dice to roll (1 to 20).
            - Set a modifier to add to the roll (-20 to 20).

        The frame is styled with a light blue background and contains labels 
        and input widgets for each option. The frame is stored in the 
        `self.frames` dictionary at index 3.

        Returns:
            None
        """
        general_frame = tb.Frame(self)
        self.frames["general"] = general_frame
        dice_type = tb.StringVar(general_frame)
        dice_type.set("d20")
        general_frame_label = tb.Label(
            general_frame,
            text="Choose your Dice: ",
            bootstyle="info",
            font=("Arial", 12, "bold")
        )
        general_frame_label.pack()
        dice_type_label = tb.Label(
            general_frame,
            text="Select the type of Dice to Roll:")
        dice_type_label.pack(side=tb.LEFT, padx=5, pady=5)
        dice_type_menu = tb.OptionMenu(
            general_frame,
            dice_type, "d4", "d6", "d8", "d10", "d12", "d20", "d100"
        )
        dice_type_menu.pack(side=tb.LEFT, padx=5, pady=5)
        number_of_dice_label = tb.Label(
            general_frame, text="How many Dice to Roll?")
        number_of_dice_label.pack()
        number_of_dice = tb.Spinbox(
            general_frame, from_=1, to=20, width=5,
            textvariable=self.number_of_dice)
        number_of_dice.pack()
        dice_modifier_label = tb.Label(
            general_frame, text="Modifier to add to the roll?")
        dice_modifier_label.pack()
        dice_modifier = tb.Spinbox(
            general_frame, from_=-20, to=20, width=5,
            textvariable=self.dice_modifier)
        dice_modifier.pack()
        general_frame.pack(fill=tb.X, pady=10)

    def create_skill_check_frame(self):
        """
        Creates and configures the skill check frame within the application UI.

        This method initializes a new Tkinter Frame for skill checks, adds a 
        label prompting the user to select a skill, and sets up a Combobox 
        populated with available skills from the Skills.ability_map. The 
        Combobox is bound to an event handler that updates the 
        advantage/disadvantage state when a skill is selected. The frame is 
        stored in the frames dictionary and packed into the main window.

        Side Effects:
            - Modifies self.frames by adding the skill check frame at index 4.
            - Initializes self.skill_combobox for later use.
            - Packs the skill check frame into the main window.
        """
        skill_check_frame = tb.Frame(self)
        self.frames["skill"] = skill_check_frame
        skill_check_label = tb.Label(
            skill_check_frame, text="Which Skill check to roll?")
        skill_check_label.pack()
        self.skill_combobox = tb.Combobox(
            skill_check_frame,
            values=list(Skills.ability_map.keys()),
            bootstyle="info"
        )
        self.skill_combobox.bind(
            "<<ComboboxSelected>>", lambda event:
                self.update_advantage_disadvantage("skill", event))
        self.skill_combobox.pack()
        skill_check_frame.pack(fill=tb.X, pady=10)

    def create_saving_throw_frame(self):
        """
        Creates and configures the saving throw selection frame in the GUI.

        This method initializes a new frame for saving throw selection, adds a 
        label prompting the user, and sets up a combobox populated with 
        available saving throw abilities. It also binds an event handler to the 
        combobox for updating advantage/disadvantage options when a selection 
        is made. The frame is then packed into the main window layout.

        Side Effects:
            - Modifies self.frames by adding the saving throw frame at index 5.
            - Initializes self.saving_throw_combobox for later use.
            - Updates the GUI layout with the new frame and widgets.
        """
        saving_throw_frame = tb.Frame(self)
        self.frames["save"] = saving_throw_frame
        saving_throw_label = tb.Label(
            saving_throw_frame,
            text="Which Saving Throw to Roll?")
        saving_throw_label.pack()
        self.saving_throw_combobox = tb.Combobox(
            saving_throw_frame, values=list(SavingThrows.ability_map.keys()))
        self.saving_throw_combobox.bind(
            "<<ComboboxSelected>>", lambda event:
                self.update_advantage_disadvantage("save", event))
        self.saving_throw_combobox.pack()
        saving_throw_frame.pack(fill=tb.X, pady=10)

    def create_weapon_attack_frame(self):
        """
        Creates and configures the weapon attack frame in the GUI.

        This frame allows the user to select a weapon from a dropdown list 
        (combobox) populated with the names of weapons available to the player 
        character. It also adds a visual separator and label for clarity.

        The frame is stored in the `self.frames` dictionary at index 6 and 
        packed into the main window.

        Returns:
            None
        """
        weapon_attack_frame = tb.Frame(self)
        self.frames["weapon"] = weapon_attack_frame
        tb.Label(weapon_attack_frame, text="Select Weapon:").pack()
        self.weapon_combobox = tb.Combobox(
           weapon_attack_frame, values=[weapon.name for weapon in self.player_character.weapons])
        self.weapon_combobox.pack()
        weapon_attack_frame.pack(fill=tb.X, pady=10)

    

    def create_special_ability_frame(self):
        """
        Creates and configures the special ability frame in the GUI.

        This frame allows the user to select a special ability from a dropdown list 
        (combobox) populated with the names of special abilities available to the player 
        character. It also adds a visual separator and label for clarity.

        The frame is stored in the `self.frames` dictionary at index 7 and 
        packed into the main window.

        Returns:
            None
        """
        special_ability_frame = tb.Frame(self)
        self.frames[7] = special_ability_frame
        tb.Label(special_ability_frame, text="Active Abilities:").pack()
        self.special_ability_combobox = tb.Combobox(
            special_ability_frame,
            values=[ability.name for ability in self.player_character.special_abilities])
        self.special_ability_combobox.pack()
        special_ability_frame.pack(fill=tb.X, pady=10)

    def create_bottom_frame(self):
        """
        Creates and configures the bottom frame of the application UI.

        This frame includes:
            - A horizontal separator for visual separation.
            - A "Roll Dice" button to trigger the dice rolling logic.
            - A "Reset" button to reset input values and results.
            - Labels for displaying advantage status, roll result, critical hit 
              status, and attack damage.

        The frame is styled with a light blue background and appropriate 
        padding.
        The created frame is stored in self.frames["bottom"].
        """
        bottom_frame = tb.Frame(self)
        self.frames["bottom"] = bottom_frame
        roll_button = tb.Button(
            bottom_frame,
            text="Roll Dice",
            command=self.roll_dice,
        )
        roll_button.pack(pady=20)
        reset_button = tb.Button(
            bottom_frame, text="Reset", command=self.reset_values, style="TButton")
        reset_button.pack(pady=5)
        self.advantage_label = tb.Label(
            bottom_frame, text="")
        self.advantage_label.pack()
        self.result_label = tb.Label(
            bottom_frame, text="")
        self.result_label.pack()
        self.crit_label = tb.Label(
            bottom_frame, text="")
        self.crit_label.pack()
        self.attack_damage_label = tb.Label(
            bottom_frame, text="")
        self.attack_damage_label.pack()
        bottom_frame.pack(fill=tb.X, pady=10)

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
        frame = self.frame_variable.get()
        if frame == "skill":
            self.frames["general"].pack_forget()
            self.frames["save"].pack_forget()
            self.frames["weapon"].pack_forget()
            self.frames["skill"].pack(before=self.frames["bottom"])
        elif frame == "save":
            self.frames["general"].pack_forget()
            self.frames["skill"].pack_forget()
            self.frames["weapon"].pack_forget()
            self.frames["save"].pack(before=self.frames["bottom"])
        elif frame == "weapon":
            self.frames["general"].pack_forget()
            self.frames["skill"].pack_forget()
            self.frames["save"].pack_forget()
            self.frames["weapon"].pack(before=self.frames["bottom"])
        else:
            self.frames["skill"].pack_forget()
            self.frames["save"].pack_forget()
            self.frames["weapon"].pack_forget()
            self.frames["general"].pack(before=self.frames["bottom"])

    def clear_labels(self):
        """
        Clears the text of all result-related labels in the UI, including 
        advantage, critical hit, result, and attack damage labels.
        """
        self.advantage_label.config(text="")
        self.crit_label.config(text="")
        self.result_label.config(text="")
        self.attack_damage_label.config(text="")

    # Helper for updating advantage label
    def update_advantage_label(self, advantage, rolls):
        """
        Updates the advantage label in the UI to display the result of an 
        advantage or disadvantage roll.

        Args:
            advantage (int): Indicates the type of roll. 
                1 for advantage, 2 for disadvantage, any other value clears the 
                label.
            rolls (list): Contains the roll values and the final result.
                Expected format: [[roll1, roll2], result].

        Returns:
            None
        """
        if advantage in (1, 2):
            roll_type = "Advantage" if advantage == 1 else "Disadvantage"
            text = f"{roll_type} Roll: {rolls[0][0]} vs {rolls[0][1]} = {rolls[1]}"
            self.advantage_label.config(text=text)
        else:
            self.advantage_label.config(text="")

    def update_crit_label(self, dice_roll):
        """
        Updates the text of the crit_label widget to display the result message 
        for a given dice roll.

        Args:
            dice_roll (int): The value of the dice roll to be displayed.

        Returns:
            None
        """
        self.crit_label.config(text=f"{Messages.result_message(dice_roll)}")

    def update_result_label(self, combobox, dice_rolls, dice_total, modifier):
        """
        Updates the result label to display the outcome of a dice roll with a 
        modifier.

        Args:
            combobox (str): The name or value selected from the combobox, 
            representing the dice type.
            dice_roll (int): The result of the dice roll.
            modifier (int): The modifier to be added or subtracted from the dice 
            roll.

        The label is updated to show the calculation in the format:
            "{combobox}: {dice_roll} + {modifier} = {total}" if modifier is 
            non-negative,
            or "{combobox}: {dice_roll} - {abs(modifier)} = {total}" if modifier 
            is negative.
        """
        total = dice_total + modifier
        sign = "+" if modifier >= 0 else "-"
        self.result_label.config(
            text=f"{combobox}: {dice_rolls} {sign} {abs(modifier)} = {total}"
        )

    def update_attack_damage_label(
        self,
        weapon_name,
        damage_rolls,
        damage_bonuses,
        total_damage
    ):
        """
        Updates the attack damage label with the provided weapon name, damage 
        rolls, bonuses, and total damage.

        Args:
            weapon_name (str): The name of the weapon.
            damage_rolls (str): The string representation of the damage rolls.
            damage_bonuses (str): The string representation of the damage 
            bonuses.
            total_damage (int or str): The total calculated damage.

        Returns:
            None
        """
        self.attack_damage_label.config(
                text=f"{weapon_name} Damage: {damage_rolls} + {damage_bonuses} = {total_damage}")


    def roll_d20_with_advantage(self, advantage):
        """
        Rolls a 20-sided die (d20) with advantage or disadvantage.

        Args:
            advantage (str): Specifies the type of roll. 
                Accepts 'advantage', 'disadvantage', or None for a normal roll.

        Returns:
            list: The result(s) of the d20 roll(s) based on the advantage 
            parameter.
        """
        rolls = self.dice.d20_roll(advantage=advantage)
        return rolls

    def general_roll(self):
        """
        Performs a general dice roll based on user input from the GUI.

        - Retrieves the dice type, number of dice, and modifier from the 
            corresponding GUI widgets.
        - Clears any previously rolled dice.
        - If rolling a single d20, checks for advantage/disadvantage and rolls 
            accordingly, updating the GUI labels for advantage and critical 
            hits.
        - Otherwise, rolls the specified number of dice of the selected type, 
            sums the results, and updates the result label with the total and 
            modifier.

        Returns:
            None
        """
        dice_type = int(self.frames["general"].children['!optionmenu'].cget('text')[1:])
        number_of_dice = int(self.frames["general"].children['!spinbox'].get())
        dice_modifier = int(self.frames["general"].children['!spinbox2'].get())
        if dice_type == 20 and number_of_dice == 1:
            advantage = self.advantage_var.get()
            rolls = self.roll_d20_with_advantage(advantage)
            self.update_advantage_label(advantage, rolls)
            roll=rolls[1]
            self.update_crit_label(roll)
            self.update_result_label(
                "General Roll", roll, roll, dice_modifier)
        else:
            for _ in range(number_of_dice):
                die = Dice(dice_type)
                self.dice.add_dice(die)
            dice_total = self.dice.total_roll()
            print(f"Dice Rolls: {dice_total[0]}, Total: {dice_total[1]}")
            self.update_result_label(
                "General Roll", dice_total[0], dice_total[1], dice_modifier)

    def calculate_attack_damage(self, weapon_name, dice_roll, dice_modifier):
        """
        Calculates the total attack damage for a given weapon and dice roll.

        This method determines the minimum attack value and damage bonus based 
        on the weapon's weight type. It parses the weapon's damage dice 
        notation, applies critical hit rules (doubling dice on a roll of 20),
        and rolls the appropriate number of dice with the specified minimum 
        value. The total damage is computed by summing the dice rolls and adding 
        relevant bonuses, then updates the attack damage label.

        Args:
            weapon_name (str): The name of the weapon used for the attack.
            dice_roll (int): The result of the attack roll (e.g., d20 roll).
            dice_modifier (int): The modifier to apply to the damage 
            calculation.

        Returns:
            None
        """
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
        Performs a d20 check for the specified check type using the selected 
        value from the combobox. Retrieves the appropriate modifier for the 
        check, determines if advantage/disadvantage applies, rolls the d20 
        accordingly, and updates the UI labels to reflect the roll, critical 
        status, and result. If the check type is "attack", calculates and 
        displays the attack damage.
        Args:
            check_type (str): The type of check to perform (e.g., "attack", 
            "skill", etc.).
            combobox (tkinter.ttk.Combobox): The combobox widget containing 
            selectable options for the check.
        Returns:
            None
        """
        selected = combobox.get()
        modifier = self.player_character.get_check_modifier(
            selected, check_type)
        advantage = self.advantage_var.get()
        rolls = self.roll_d20_with_advantage(advantage)
        self.update_advantage_label(advantage, rolls)

        roll=rolls[1]
        self.update_crit_label(roll)
        self.update_result_label(selected, roll, roll, modifier)
        if check_type == "attack":
            self.calculate_attack_damage(
                selected,
                roll,
                modifier
            )

    def reset_values(self):
        """Set default values for all inputs."""
        self.frame_variable.set("general")
        self.show_frame()
        self.skill_combobox.set("Animal Handling")
        self.saving_throw_combobox.set("Strength")
        self.weapon_combobox.set("Glaive")
        self.advantage_var.set(0)
        self.clear_labels()

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
        self.dice.clear_dice()  # Clear previous dice rolls
        frame = self.frame_variable.get()
        if frame == "skill":
            self.d20_check("skill", self.skill_combobox)
        elif frame == "save":
            self.d20_check("save", self.saving_throw_combobox)
        elif frame == "weapon":
            self.d20_check("attack", self.weapon_combobox)
        else:  # "general"
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
    Warryn.save_bonus += 1
    Warryn.add_weapon(Weapon("Glaive", "martial", "slashing", "1d10", weight_type="Heavy"))
    Warryn.add_weapon(Weapon("Maul", "martial", "bludgeoning", "2d6", weight_type="Heavy"))
    Warryn.add_weapon(Weapon("Longbow","martial", "piercing", "1d8", weight_type="Heavy"))
    Warryn.add_weapon(Weapon("Spear","Simple", "piercing", "1d8", weight_type="Normal"))
    app = DiceRollerApp(player_character=Warryn)
    app.mainloop()
