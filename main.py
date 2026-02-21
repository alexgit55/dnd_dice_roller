import FreeSimpleGUI as sg

from dice import Die, DiceRoller
from messages import Messages
from roll import RollManager, RollResult, Roll


class MainWindow:
    """
    Manages the graphical user interface (GUI) for a dice rolling application.

    This class initializes and provides functionality for a PySimpleGUI-based
    interface to roll dice, manage roll presets, and display roll history. The
    application supports normal rolls, advantage/disadvantage rolls, and includes
    options to save, load, and edit roll presets.

    :ivar roller: Utility object to manage dice rolling logic.
    :type roller: DiceRoller
    :ivar roll_history: Manager for storing and retrieving the history of dice rolls.
    :type roll_history: RollManager
    :ivar roll_presets: Manager for handling save/load functionality of roll presets.
    :type roll_presets: RollManager
    :ivar layout: Defines the layout structure of the GUI components.
    :type layout: list
    :ivar window: Main GUI window for the dice rolling application.
    :type window: sg.Window
    """
    def __init__(self):
        self.roller = DiceRoller()
        sg.theme('DarkGrey15')
        self.roll_history = RollManager()
        self.roll_presets = RollManager()
        self.roll_presets.load_from_file('presets.json')
        self.roll_result_messages = Messages()
        self.layout = [
            [
                sg.Frame('Roll Presets',
                         layout=[
                             [
                                 sg.Radio("Skills",
                                          key='skill_presets',
                                          group_id='preset_type',
                                          default=True,
                                          enable_events=True),
                                 sg.Radio("Saves",
                                          key='save_presets',
                                          group_id='preset_type',
                                          default=False,
                                          enable_events=True),
                                 sg.Radio("Abilities",
                                          key='ability_presets',
                                          group_id='preset_type',
                                          default=False,
                                          enable_events=True),
                                 sg.Radio("Custom",
                                          key='custom_presets',
                                          group_id='preset_type',
                                          default=False,
                                          enable_events=True),
                             ],
                             [sg.Listbox(values=self.roll_presets.get_rolls(roll_type='skill'),
                                         size=(40, 10),
                                         key='roll_preset',
                                         auto_size_text=True,
                                         horizontal_scroll=True,
                                         enable_events=True,
                                         tooltip='Click to load a roll into the dice roller.')
                             ],
                             [
                                 sg.Push(),
                                 sg.Button('Edit Preset',
                                           key='edit_preset'),
                                 sg.Button('Remove Preset',
                                           key='remove_preset'),
                                 sg.Push(),
                             ],
                         ],
                ),
                sg.Frame('Dice Roller',
                layout=
                [
                    [
                        sg.Push(),
                        sg.Column(
                            layout=[
                                [sg.Text('How many Dice to Roll?')],
                                [
                                    sg.Push(),
                                    sg.Spin(values=[i for i in range(1,20)],
                                        initial_value=1,
                                        key='dice_count',
                                        size=(5, 1),),
                                    sg.Push()
                                ],
                                [sg.Text("Select the type of Dice to Roll:")],
                                [
                                    sg.Push(),
                                    sg.Combo(values=Die.get_dice_types(),
                                          default_value='d20',
                                          auto_size_text=True,
                                          key='dice_type',
                                          readonly=True,
                                          enable_events=True),
                                    sg.Push()
                                ],
                                [sg.Text("Modifier to add to the roll?")],
                                [
                                    sg.Push(),
                                    sg.Spin(values=[i for i in range(-20, 20)],
                                         key='dice_modifier',
                                         initial_value=0,
                                         size=(5, 1), ),
                                    sg.Push()
                                ]
                            ]),
                        sg.Push(),
                    ],
                    [sg.HorizontalSeparator()],
                    [
                        sg.Push(),
                        sg.Radio("Normal",
                            key='normal_roll',
                            group_id='advantage',
                            default=True),
                        sg.Radio("Advantage",
                            key='advantage_roll',
                            group_id='advantage',
                            default=False),
                        sg.Radio("Disadvantage",
                                 key='disadvantage_roll',
                                 group_id='advantage',
                                 default=False),
                        sg.Push(),
                    ],
                    [sg.HorizontalSeparator()],
                    [
                        sg.Push(),
                        sg.Button("Roll Dice",
                                  key='roll',
                                  font=('Helvetica', 12, 'bold'),
                                  size=(10, 1)),
                        sg.Push()
                    ],
                    [
                        sg.Push(),
                        sg.Button("Save As Preset", key="save_preset"),
                        sg.Button("Reset", key='reset'),
                        sg.Push(),
                    ],
                    [
                        sg.Push(),
                        sg.Frame('Result',
                                 layout=[
                                     [sg.Text('', key='advantage_text')],
                                     [
                                         sg.Text('',
                                                 key='total_text',
                                                 font=('Helvetica', 16, 'bold')),
                                         sg.Text('',
                                                 key='equal_sign',
                                                 font=('Helvetica', 16, 'bold')),
                                         sg.Text('',
                                                 key='dice_total',
                                                 font=('Helvetica', 18, 'bold'),
                                                 text_color='red')

                                    ],
                                     [sg.Text('', key='message_text')]
                                 ]
                                 ),
                        sg.Push(),
                    ]
                ]),
             sg.Frame('Roll History',
                      layout=[
                          [sg.Listbox(values=self.roll_history.get_rolls(),
                                      size=(40, 10),
                                      key='roll_history',
                                      auto_size_text=True,
                                      horizontal_scroll=True,
                                      enable_events=True,
                                      tooltip='Click to load a roll into the dice roller.')],
                          [
                              sg.Push(),
                              sg.Button('Clear History', key='clear_history'),
                              sg.Push(),
                          ],
                      ],
                      )
            ],
            [
                sg.StatusBar('Ready',
                             key='status_bar',
                             size=(40, 1)
                             ),
                sg.Push(),
                sg.Button('Exit', key='exit')]
        ]

        self.window = sg.Window('Dice Roller Application', self.layout)

    def run(self):
        """
        Executes the main event loop to handle user interaction within the application window.

        This method continuously listens for events triggered by user actions on the GUI and delegates
        handling these events to corresponding functions. The loop runs indefinitely until the window
        is closed or an exit event is triggered. The method provides functionality to handle dice rolls,
        resetting configurations, managing roll history, and performing CRUD operations on presets.

        :raises KeyError: If an invalid option or key is encountered during event handling.
        """
        current_preset = None
        while True:
            event, values = self.window.read()
            match event:
                case 'skill_presets' | 'save_presets' | 'ability_presets' | 'custom_presets':
                    current_preset = None
                    self.refresh_roll_presets_list()
                case 'roll':
                    self.roll_dice()
                case 'reset':
                    self.reset_to_default()
                case 'clear_history':
                    self.clear_roll_history()
                case 'roll_history':
                    roll = values['roll_history'][0]
                    self.load_preset(roll)
                case 'roll_preset':
                    current_preset = values['roll_preset'][0]
                    self.load_preset(current_preset)
                case 'save_preset':
                    self.save_preset()
                case 'edit_preset':
                    if current_preset is None:
                        sg.popup_ok('Please select a preset to edit.')
                        continue
                    self.edit_preset(current_preset)
                case 'remove_preset':
                    if current_preset is None:
                        sg.popup_ok('Please select a preset to remove.')
                        continue
                    self.remove_preset(current_preset)
                case _ if event in (sg.WIN_CLOSED, 'exit'):
                    break

        self.window.close()

    def roll_dice(self):
        """
        Rolls dice based on user input and updates the roll results accordingly.

        This method processes the dice rolling logic. Depending on the user's selected
        dice type, the number of dice, and any modifiers, it calculates the outcomes of
        the rolls, considers cases like advantage roll for a single d20, and updates
        the results through the corresponding method.

        :raises ValueError: Raised if the input values for the dice count or modifier
            cannot be parsed as integers.
        :raises AttributeError: Raised if required attributes from the user interface
            (e.g., `dice_count`, `dice_modifier`, or `dice_type`) are not properly defined.

        :return: None
        """
        self.roller.clear_dice()
        num_dice=int(self.window['dice_count'].get())
        dice_modifier=int(self.window['dice_modifier'].get())
        dice_type = self.window['dice_type'].get()
        if dice_type == 'd20' and num_dice == 1:
            rolls=self.get_advantage_roll()
            dice_total=rolls[1]
            roll_result = RollResult(num_dice, dice_type, rolls, dice_modifier, dice_total)
            self.update_results(roll_result)
        else:
            for _ in range(num_dice):
                self.roller.add_dice(Die(dice_type))
            dice_total = self.roller.total_roll()
            roll_result = RollResult(num_dice, dice_type, dice_total[0], dice_modifier, dice_total[1])
            self.update_results(roll_result)

    def get_preset_selection(self):
        """
        Determines the type of preset selected by the user from the provided GUI window.

        This method evaluates the state of specific GUI elements to decide which preset type
        is currently selected. If none of the predefined preset types are active, it defaults
        to returning 'custom'.

        :return: A string representing the selected preset type. Possible values are:
         'skill', 'save', 'ability', or 'custom'.
        :rtype: str
        """
        if self.window['skill_presets'].get():
            return 'skill'
        elif self.window['save_presets'].get():
            return 'save'
        elif self.window['ability_presets'].get():
            return 'ability'
        return 'custom'

    def refresh_roll_presets_list(self):
        """
        Refreshes the roll presets dropdown list in the user interface based on the selected roll type.

        This method retrieves the currently selected roll type from the preset selection, fetches the associated
        list of roll presets, and updates the dropdown widget in the user interface with this new list. It also
        clears any previous selection to ensure stale presets are not used inadvertently.

        :raises KeyError: If the required key for updating the user interface is not found.
        :return: None
        """
        roll_type = self.get_preset_selection()
        self.window['roll_preset'].update(values=self.roll_presets.get_rolls(roll_type=roll_type))
        self.window['roll_preset'].update(set_to_index=[])  # clear selection so you don’t load stale preset

    def get_advantage_selection(self):
        """
        Determines the type of roll selection (advantage, disadvantage, or normal roll)
        based on the current state of the application window.

        The method checks specific conditions determined by the application window settings to
        return the appropriate selection, which can be either an advantage roll, disadvantage roll,
        or a normal roll as default.

        :return: A string indicating the roll selection type. Possible values are:
                 'advantage_roll', 'disadvantage_roll', or 'normal_roll'.
        :rtype: str
        """
        if self.window['advantage_roll'].get():
            return 'advantage_roll'
        elif self.window['disadvantage_roll'].get():
            return 'disadvantage_roll'
        return 'normal_roll'

    def get_advantage_roll(self):
        """
        Computes and returns a dice roll based on the current advantage or disadvantage settings.

        The method evaluates whether an advantage or disadvantage roll should be performed based on
        flags in the `window` attribute. It executes a dice roll using the `roller` object and returns
        the result based on the settings. If neither advantage nor disadvantage is selected, a regular
        roll is executed.

        :return: The result of the dice roll. The roll may include an advantage, a disadvantage, or
            be a regular roll depending on the current state.
        :rtype: int
        """
        if self.window['advantage_roll'].get():
            return self.roller.d20_roll(advantage=1)
        elif self.window['disadvantage_roll'].get():
            return self.roller.d20_roll(advantage=2)
        return self.roller.d20_roll()

    def update_results(self, roll_result: RollResult):
        """
        Updates the result displays and adjusts any relevant roll outcome details based on the current
        status of advantage or disadvantage selections. Also updates roll-specific messages and maintains
        the roll history.

        :param roll_result: An instance of RollResult encapsulating details about the result of the dice roll.
        :type roll_result: RollResult
        """
        if self.window['advantage_roll'].get():
            roll_result.advantage = "advantage_roll"
            self.window['advantage_text'].update(value="Rolling with Advantage")
        elif self.window['disadvantage_roll'].get():
            roll_result.advantage = "disadvantage_roll"
            self.window['advantage_text'].update(value="Rolling with Disadvantage")
        else:
            self.window['advantage_text'].update(value="")

        self.window['total_text'].update(value=f'{roll_result.get_shorthand()}')
        self.window['equal_sign'].update(value='=')
        self.window['dice_total'].update(value=f'{roll_result.total}')

        if roll_result.num_dice == 1 and self.window['dice_type'].get() == 'd20':
            result_message = self.roll_result_messages.result_message(roll_result.dice_total)
            self.window['message_text'].update(value=f'{result_message}')
        else:
            self.window['message_text'].update(value="")

        self.update_roll_history(roll_result)

    def update_roll_history(self, roll_result):
        """
        Updates the roll history with a new roll result and refreshes the associated
        UI element to display the updated history.

        :param roll_result: The result of the roll to be added to the history.
        :type roll_result: int
        :return: None
        """
        self.roll_history.add_roll(roll_result)
        self.window['roll_history'].update(values=self.roll_history.get_rolls())

    def clear_roll_history(self):
        """
        Clears the roll history and updates the UI components accordingly.

        This method resets the roll history data by clearing it and then updating
        the relevant user interface elements, including the roll history display
        and the status bar message.

        :return: None
        """
        self.roll_history.clear()
        self.window['roll_history'].update(values=self.roll_history.get_rolls())

        self.window['status_bar'].update(f'Roll History Cleared')

    def reset_to_default(self):
        """
        Resets the application interface to its default settings.

        This method updates various UI elements to default values in the application. It
        clears input fields, resets roll options to their initial state, and restores
        the system status to indicate that default settings have been restored.

        :return: None
        """
        self.window['advantage_roll'].update(value=False)
        self.window['disadvantage_roll'].update(value=False)
        self.window['normal_roll'].update(value=True)
        self.window['advantage_text'].update(value="")
        self.window['total_text'].update(value="")
        self.window['message_text'].update(value="")
        self.window['dice_modifier'].update(value=0)
        self.window['dice_count'].update(value=1)
        self.window['dice_type'].update(value='d20')
        self.window['equal_sign'].update(value='')
        self.window['dice_total'].update(value='')

        self.window['status_bar'].update(f'Default Settings Restored')

    def save_preset(self):
        """
        Prompts the user to save a roll configuration as a preset, ensuring the preset
        has a unique name, and then persists the preset to a JSON file. Updates the
        application's status bar and preset dropdown to reflect the new addition.

        :param self: The instance of the class where this method is defined.
        :type self: object

        :return: None
        """
        # Prompt user for preset name, if user clicks cancel, return without saving
        preset_name = sg.popup_get_text('Enter a name for the preset:')
        if preset_name is None:
            return

        # Check if preset already exists
        if preset_name in self.roll_presets.get_rolls():
           sg.popup_ok('Preset already exists. Please choose a different name.')

        roll = Roll(num_dice=self.window['dice_count'].get(),
                    dice_type=self.window['dice_type'].get(),
                    dice_modifier=self.window['dice_modifier'].get(),
                    advantage=self.get_advantage_selection(),
                    name=preset_name,
                    roll_type="custom")
        self.roll_presets.add_roll(roll)
        self.roll_presets.save_to_file('presets.json')
        self.roll_presets.load_from_file('presets.json')
        self.window['status_bar'].update(f'Preset {roll.name} Added Successfully')

        self.window['roll_preset'].update(values=self.roll_presets.get_rolls())

    def edit_preset(self, roll):
        """
        Edits an existing preset defined by the `roll` object. This method allows the
        user to modify the roll's name, advantage, number of dice, dice type, and
        dice modifier through user input and updates the preset collection accordingly.

        :param roll: The roll object representing the preset to be edited.
        :type roll: object
        :return: None
        """
        # Prompt user for preset name
        preset_name = sg.popup_get_text('Enter a name for the preset:',
                                        default_text=roll.name)
        roll.name = preset_name
        roll.advantage = self.get_advantage_selection()
        roll.num_dice = self.window['dice_count'].get()
        roll.dice_type = self.window['dice_type'].get()
        roll.dice_modifier = self.window['dice_modifier'].get()
        index = self.roll_presets.get_roll_index(roll)
        self.roll_presets.update_roll(roll, index)

        self.roll_presets.save_to_file('presets.json')
        self.roll_presets.load_from_file('presets.json')
        self.window['roll_preset'].update(values=self.roll_presets.get_rolls())
        self.window['status_bar'].update(f'Preset {roll.name} Updated Successfully')


    def remove_preset(self, roll):
        """
        Removes a preset from the `roll_presets`, updates the `roll_preset` dropdown, and displays a status
        message confirming the removal.

        Prompt the user for confirmation before removing the preset. If the user confirms, the specified
        preset is located by its index, removed from the preset list, and the updated list is saved to a
        file named `presets.json`. This updated list is then loaded back and the relevant UI components
        are refreshed.

        :param roll: The preset object to be removed.

        :return: None
        """
        if roll.roll_type == 'custom':
            confirmation = sg.popup_yes_no(f'Are you sure you want to remove preset "{roll.name}"?')
            if confirmation == 'Yes':
                index = self.roll_presets.get_roll_index(roll)
                self.roll_presets.remove_roll(index)
                self.roll_presets.save_to_file('presets.json')
                self.roll_presets.load_from_file('presets.json')
                self.window['roll_preset'].update(values=self.roll_presets.get_rolls())

                self.window['status_bar'].update(f'Preset {roll.name} Removed Successfully')
        else:
            sg.popup_ok('Cannot remove built-in presets.')

    def load_preset(self, roll):
        """
        Updates the UI components with the preset values from the provided roll object.

        :param roll: An object containing the following attributes:
            - dice_modifier: Modifier value to adjust the dice roll.
            - num_dice: Number of dice to roll.
            - dice_type: Type of dice to use for the roll.
            - advantage: A string key indicating the UI element that corresponds
              to the roll's advantage setting.
        :return: None
        """
        self.window['dice_modifier'].update(value=roll.dice_modifier)
        self.window['dice_count'].update(value=roll.num_dice)
        self.window['dice_type'].update(value=roll.dice_type)
        self.window[f'{roll.advantage}'].update(value=True)


if __name__ == '__main__':
    window = MainWindow()
    window.run()