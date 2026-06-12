import FreeSimpleGUI as sg

from domain.models.character_traits import SavingThrows, Skills


ABILITY_NAMES = [
    "Strength",
    "Dexterity",
    "Constitution",
    "Intelligence",
    "Wisdom",
    "Charisma",
]


def build_layout(character=None):
    """
    Builds the character create/edit window layout.

    :param character: Optional Character object. If provided, the form is pre-filled
        for editing. If omitted, the form is initialized for creating a new character.
    :return: A FreeSimpleGUI layout.
    """
    name = character.name if character else ""
    character_id = character.character_id if character else ""
    proficiency_bonus = character.proficiency_bonus if character else 2
    save_bonus = character.save_bonus if character else 0

    ability_scores = character.ability_scores if character else {}

    skill_names = list(Skills.ability_map.keys())
    saving_throw_names = list(SavingThrows.ability_map.keys())

    selected_skill_proficiencies = (
        character.skills.get_proficiencies()
        if character
        else []
    )
    selected_skill_advantages = (
        character.skills.get_advantages()
        if character
        else []
    )
    selected_skill_disadvantages = (
        character.skills.get_disadvantages()
        if character
        else []
    )

    selected_save_proficiencies = (
        character.saving_throws.get_proficiencies()
        if character
        else []
    )
    selected_save_advantages = (
        character.saving_throws.get_advantages()
        if character
        else []
    )
    selected_save_disadvantages = (
        character.saving_throws.get_disadvantages()
        if character
        else []
    )

    basic_info_frame = sg.Frame(
        "Basic Info",
        layout=[
            [
                sg.Text("Name:", size=(16, 1)),
                sg.Input(
                    default_text=name,
                    key="character_name",
                    size=(30, 1),
                ),
            ],
            [
                sg.Text("Character ID:", size=(16, 1)),
                sg.Input(
                    default_text=character_id,
                    key="character_id",
                    size=(30, 1),
                    disabled=True,
                ),
            ],
            [
                sg.Text("Proficiency Bonus:", size=(16, 1)),
                sg.Spin(
                    values=[i for i in range(0, 11)],
                    initial_value=proficiency_bonus,
                    key="proficiency_bonus",
                    size=(5, 1),
                ),
            ],
            [
                sg.Text("Save Bonus:", size=(16, 1)),
                sg.Spin(
                    values=[i for i in range(-10, 11)],
                    initial_value=save_bonus,
                    key="save_bonus",
                    size=(5, 1),
                ),
            ],
        ],
    )

    ability_score_frame = sg.Frame(
        "Ability Scores",
        layout=[
            [
                sg.Text(ability_name, size=(14, 1)),
                sg.Spin(
                    values=[i for i in range(1, 31)],
                    initial_value=ability_scores.get(ability_name, 10),
                    key=f"ability_{ability_name}",
                    size=(5, 1),
                ),
            ]
            for ability_name in ABILITY_NAMES
        ],
    )

    skill_frame = sg.Frame(
        "Skills",
        layout=[
            [
                sg.Text("Proficient", size=(24, 1)),
                sg.Text("Advantage", size=(24, 1)),
                sg.Text("Disadvantage", size=(24, 1)),
            ],
            [
                sg.Listbox(
                    values=skill_names,
                    default_values=selected_skill_proficiencies,
                    select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                    key="skill_proficiencies",
                    size=(24, 12),
                ),
                sg.Listbox(
                    values=skill_names,
                    default_values=selected_skill_advantages,
                    select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                    key="skill_advantages",
                    size=(24, 12),
                ),
                sg.Listbox(
                    values=skill_names,
                    default_values=selected_skill_disadvantages,
                    select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                    key="skill_disadvantages",
                    size=(24, 12),
                ),
            ],
        ],
    )

    saving_throw_frame = sg.Frame(
        "Saving Throws",
        layout=[
            [
                sg.Text("Proficient", size=(24, 1)),
                sg.Text("Advantage", size=(24, 1)),
                sg.Text("Disadvantage", size=(24, 1)),
            ],
            [
                sg.Listbox(
                    values=saving_throw_names,
                    default_values=selected_save_proficiencies,
                    select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                    key="save_proficiencies",
                    size=(24, 6),
                ),
                sg.Listbox(
                    values=saving_throw_names,
                    default_values=selected_save_advantages,
                    select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                    key="save_advantages",
                    size=(24, 6),
                ),
                sg.Listbox(
                    values=saving_throw_names,
                    default_values=selected_save_disadvantages,
                    select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                    key="save_disadvantages",
                    size=(24, 6),
                ),
            ],
        ],
    )

    return [
        [
            sg.Text(
                "Character Editor",
                font=("Arial", 16, "bold"),
            ),
        ],
        [
            basic_info_frame,
            ability_score_frame,
        ],
        [
            skill_frame,
        ],
        [
            saving_throw_frame,
        ],
        [
            sg.StatusBar(
                "Ready",
                key="status_bar",
                size=(40, 1),
            ),
            sg.Push(),
            sg.Button(
                "Save Character",
                key="save_character",
            ),
            sg.Button(
                "Cancel",
                key="cancel",
            ),
        ],
    ]