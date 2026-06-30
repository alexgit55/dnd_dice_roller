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

def skill_key(prefix, skill_name):
    return f"{prefix}_{skill_name}"

def save_key(prefix, save_name):
    return f"{prefix}_{save_name}"

def build_skill_rows(
    skill_names,
    selected_skill_proficiencies,
    selected_skill_expertise,
    selected_skill_advantages,
    selected_skill_disadvantages,
):
    rows = [
        [
            sg.Push(),
            sg.Text("Skill", size=(20, 1), font=("Arial", 14, "bold")),
            sg.Text("Proficiency", size=(20, 1), font=("Arial", 14, "bold")),
            sg.Text("Roll State", size=(20, 1), font=("Arial", 14, "bold")),
        ]
    ]

    for skill_name in skill_names:
        proficiency_group = f"skill_proficiency_{skill_name}"
        advantage_group = f"skill_advantage_{skill_name}"

        has_expertise = skill_name in selected_skill_expertise
        is_proficient = skill_name in selected_skill_proficiencies and not has_expertise
        has_advantage = skill_name in selected_skill_advantages
        has_disadvantage = skill_name in selected_skill_disadvantages

        rows.append(
            [
                sg.Text(skill_name, size=(20, 1)),
                sg.Radio(
                    "None",
                    proficiency_group,
                    default=not is_proficient and not has_expertise,
                    key=skill_key("skill_prof_none", skill_name),
                ),
                sg.Radio(
                    "Proficient",
                    proficiency_group,
                    default=is_proficient,
                    key=skill_key("skill_prof_proficient", skill_name),
                ),
                sg.Radio(
                    "Expertise",
                    proficiency_group,
                    default=has_expertise,
                    key=skill_key("skill_prof_expertise", skill_name),
                ),
                sg.Push(),
                sg.Radio(
                    "None",
                    advantage_group,
                    default=not has_advantage and not has_disadvantage,
                    key=skill_key("skill_adv_none", skill_name),
                ),
                sg.Radio(
                    "Advantage",
                    advantage_group,
                    default=has_advantage,
                    key=skill_key("skill_adv_advantage", skill_name),
                ),
                sg.Radio(
                    "Disadvantage",
                    advantage_group,
                    default=has_disadvantage,
                    key=skill_key("skill_adv_disadvantage", skill_name),
                ),
            ]
        )
        rows.append([sg.HorizontalSeparator()])

    return rows

def build_saving_throw_rows(
    saving_throw_names,
    selected_save_proficiencies,
    selected_save_advantages,
    selected_save_disadvantages,
):
    rows = [
        [
            sg.Text("Saving Throw", size=(20, 1), font=("Arial", 14, "bold")),
            sg.Text("Proficiency", size=(20, 1), font=("Arial", 14, "bold")),
            sg.Text("Roll State", size=(20, 1), font=("Arial", 14, "bold"))
        ]
    ]

    for save_name in saving_throw_names:
        proficiency_group = f"save_proficiency_{save_name}"
        advantage_group = f"save_advantage_{save_name}"

        is_proficient = save_name in selected_save_proficiencies
        has_advantage = save_name in selected_save_advantages
        has_disadvantage = save_name in selected_save_disadvantages

        rows.append(
            [
                sg.Text(save_name, size=(20, 1)),
                sg.Radio(
                    "None",
                    proficiency_group,
                    default=not is_proficient,
                    key=save_key("save_prof_none", save_name),
                ),
                sg.Radio(
                    "Proficient",
                    proficiency_group,
                    default=is_proficient,
                    key=save_key("save_prof_proficient", save_name),
                ),
                sg.Push(),
                sg.Radio(
                    "None",
                    advantage_group,
                    default=not has_advantage and not has_disadvantage,
                    key=save_key("save_adv_none", save_name),
                ),
                sg.Radio(
                    "Advantage",
                    advantage_group,
                    default=has_advantage,
                    key=save_key("save_adv_advantage", save_name),
                ),
                sg.Radio(
                    "Disadvantage",
                    advantage_group,
                    default=has_disadvantage,
                    key=save_key("save_adv_disadvantage", save_name),
                ),
            ]
        )
        rows.append([sg.HorizontalSeparator()])

    return rows

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
    selected_skill_expertise = (
        character.skills.get_expertise()
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
                sg.Column(
                    build_skill_rows(
                        skill_names,
                        selected_skill_proficiencies,
                        selected_skill_expertise,
                        selected_skill_advantages,
                        selected_skill_disadvantages,
                    ),
                    scrollable=True,
                    vertical_scroll_only=True,
                    size=(780, 360),
                ),
            ],
        ],
    )

    saving_throw_frame = sg.Frame(
        "Saving Throws",
        layout=[
            [
                sg.Column(
                    build_saving_throw_rows(
                        saving_throw_names,
                        selected_save_proficiencies,
                        selected_save_advantages,
                        selected_save_disadvantages,
                    ),
                    scrollable=True,
                    vertical_scroll_only=True,
                    size=(780, 180),
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