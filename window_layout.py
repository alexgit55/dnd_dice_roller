import FreeSimpleGUI as sg

from dice import Die
from ui_settings import UISettings


def build_layout(*, preset_values, history_values):
    """
    Builds and returns the layout for a graphical user interface that enables users to define roll presets, roll dice, and view roll history.

    The layout includes the following components:
    - A "Roll Presets" section to manage predefined roll configurations. Users can select or edit preset configurations.
    - A "Dice Roller" section with controls to specify the number of dice, their type, modifiers, and rolling options such as advantage/disadvantage.
    - A "Roll History" section to display and manage the history of previously executed rolls.
    - Status information and common actions like exiting the interface.

    :param preset_values: A list of predefined roll configuration values to populate the preset list.
    :type preset_values: list[str]
    :param history_values: A list of previous roll results to populate the roll history section.
    :type history_values: list[str]
    :return: The generated graphical layout for the interface.
    :rtype: list[sg.Element]
    """
    return [
        [
            sg.Frame(
                "Roll Presets",
                layout=[
                    [
                        sg.Radio(
                            "Skills",
                            key="skill_presets",
                            group_id="preset_type",
                            default=True,
                            enable_events=True,
                        ),
                        sg.Radio(
                            "Saves",
                            key="save_presets",
                            group_id="preset_type",
                            default=False,
                            enable_events=True,
                        ),
                        sg.Radio(
                            "Abilities",
                            key="ability_presets",
                            group_id="preset_type",
                            default=False,
                            enable_events=True,
                        ),
                        sg.Radio(
                            "Custom",
                            key="custom_presets",
                            group_id="preset_type",
                            default=False,
                            enable_events=True,
                        ),
                    ],
                    [
                        sg.Listbox(
                            values=preset_values,
                            size=(40, 10),
                            key="roll_preset",
                            auto_size_text=True,
                            horizontal_scroll=True,
                            enable_events=True,
                            tooltip="Click to load a roll into the dice roller.",
                        )
                    ],
                    [
                        sg.Push(),
                        sg.Button("Edit Preset",
                                  key="edit_preset"),
                        sg.Button("Remove Preset",
                                  key="remove_preset"),
                        sg.Push(),
                    ],
                ],
            ),
            sg.Frame(
                "Dice Roller",
                layout=[
                    [
                        sg.Push(),
                        sg.Column(
                            layout=[
                                [sg.Text("How many Dice to Roll?")],
                                [
                                    sg.Push(),
                                    sg.Spin(
                                        values=[i for i in range(1, 20)],
                                        initial_value=1,
                                        key="dice_count",
                                        size=(5, 1),
                                    ),
                                    sg.Push(),
                                ],
                                [sg.Text("Select the type of Dice to Roll:")],
                                [
                                    sg.Push(),
                                    sg.Combo(
                                        values=Die.get_dice_types(),
                                        default_value="d20",
                                        auto_size_text=True,
                                        key="dice_type",
                                        readonly=True,
                                        enable_events=True,
                                    ),
                                    sg.Push(),
                                ],
                                [sg.Text("Modifier to add to the roll?")],
                                [
                                    sg.Push(),
                                    sg.Spin(
                                        values=[i for i in range(-20, 20)],
                                        key="dice_modifier",
                                        initial_value=0,
                                        size=(5, 1),
                                    ),
                                    sg.Push(),
                                ],
                            ]
                        ),
                        sg.Push(),
                    ],
                    [sg.HorizontalSeparator()],
                    [
                        sg.Push(),
                        sg.Radio("Normal",
                                 key="normal_roll",
                                 group_id="advantage",
                                 default=True),
                        sg.Radio("Advantage",
                                 key="advantage_roll",
                                 group_id="advantage",
                                 default=False),
                        sg.Radio("Disadvantage",
                                 key="disadvantage_roll",
                                 group_id="advantage",
                                 default=False),
                        sg.Push(),
                    ],
                    [sg.HorizontalSeparator()],
                    [
                        sg.Push(),
                        sg.Button("Roll Dice",
                                  key="roll",
                                  font=UISettings.bold_font,
                                  size=(10, 1)),
                        sg.Push(),
                    ],
                    [
                        sg.Push(),
                        sg.Button("Save As Preset",
                                  key="save_preset"),
                        sg.Button("Reset",
                                  key="reset"),
                        sg.Push(),
                    ],
                    [
                        sg.Push(),
                        sg.Frame(
                            "Result",
                            layout=[
                                [sg.Text("",
                                         key="advantage_text")],
                                [
                                    sg.Text("",
                                            key="total_text",
                                            font=UISettings.large_font),
                                    sg.Text("",
                                            key="equal_sign",
                                            font=UISettings.bold_font),
                                    sg.Text("",
                                            key="dice_total",
                                            font=UISettings.roll_result_font,
                                            text_color="red"),
                                ],
                                [sg.Text("", key="message_text")],
                            ],
                        ),
                        sg.Push(),
                    ],
                ],
            ),
            sg.Frame(
                "Roll History",
                layout=[
                    [
                        sg.Listbox(
                            values=history_values,
                            size=(40, 10),
                            key="roll_history",
                            auto_size_text=True,
                            horizontal_scroll=True,
                            enable_events=True,
                            tooltip="Click to load a roll into the dice roller.",
                        )
                    ],
                    [
                        sg.Push(),
                        sg.Button("Clear History", key="clear_history"),
                        sg.Push(),
                    ],
                ],
            ),
        ],
        [
            sg.StatusBar("Ready", key="status_bar", size=(40, 1)),
            sg.Push(),
            sg.Button("Exit", key="exit"),
        ],
    ]