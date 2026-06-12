# DnD Dice Roller

A lightweight desktop dice-rolling app for Dungeons & Dragons and other tabletop RPGs with a simple GUI.

## Features

- Roll common dice types:
  - d4
  - d6
  - d8
  - d10
  - d12
  - d20
  - d100
- Roll multiple dice at once
- Add positive or negative modifiers
- d20 support for:
  - Normal rolls
  - Advantage
  - Disadvantage
- Optional AI-style result messages for d20 rolls
- Roll history panel
  - View previous rolls
  - Click history entries to reload roll settings
  - Clear roll history
- Roll presets:
  - Save current roll settings as a custom preset
  - Edit custom presets
  - Remove custom presets
  - Use character-based default presets
- Character management:
  - Load/select a character for the current session
  - Create new characters
  - Edit existing characters
  - Delete characters
  - Use a built-in default character
- Character-based roll presets:
  - Skill checks
  - Saving throws
  - Ability checks
- Character data includes:
  - Name
  - Character ID
  - Ability scores
  - Proficiency bonus
  - Saving throw bonus
  - Skill proficiencies
  - Skill advantages/disadvantages
  - Saving throw proficiencies
  - Saving throw advantages/disadvantages

## Character Support

The application supports multiple saved characters. A selected character affects generated default presets for skills, saving throws, and ability checks.

For example, if a character is proficient in Athletics and has a high Strength score, the Athletics preset will automatically include the correct modifier.

### Default Character

The app includes a built-in default character. This character is intended as a neutral fallback so the dice roller can always start successfully.

The default character uses:

- Ability scores of 10
- Proficiency bonus of 0
- Saving throw bonus of 0
- No skill proficiencies
- No saving throw proficiencies
- No advantages or disadvantages

The default character cannot be edited or deleted.

### Character IDs

Characters use IDs in the format:

```text
c-001 c-002 c-003
```

The default character uses:

```text
default
```

When a new character is created, the app generates the next available character ID based on the highest existing numbered character ID.

## Data Storage

The app stores user data locally in JSON files.

- `data/characters.json` — saved character data
- `data/presets.json` — saved roll presets

Character data is saved in a structured JSON format using the character model's serialization logic.

Preset data is saved separately and can be associated with a specific character.

## Requirements

- Python 3.14+
- Dependencies listed in `requirements.txt`

## Setup

Create and activate a virtual environment, then install dependencies.

### 1) Create a virtual environment

```bash
python -m venv venv
```

### 2) Activate the virtual environment

**Windows PowerShell:**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
.venv\Scripts\Activate.bat
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

## Run the App

From the project directory:

```bash
python main.py
```

## Basic Usage

### Rolling Dice

1. Choose the number of dice.
2. Choose the die type.
3. Set an optional modifier.
4. Choose normal, advantage, or disadvantage.
5. Click **Roll Dice**.

The result appears in the result panel and is added to the roll history.

### Using Roll Presets

The preset section includes multiple preset categories:

- **Skills**
- **Saves**
- **Abilities**
- **Custom**

Skill, save, and ability presets are generated from the currently loaded character.

Custom presets can be created from the current dice roller settings.

### Creating a Custom Preset

1. Configure the dice roller settings.
2. Click **Save As Preset**.
3. Enter a preset name.
4. The preset is saved and can be reused later.

### Editing or Removing a Preset

Only custom presets can be edited or removed.

Built-in character-based presets cannot be manually edited or deleted because they are generated from the active character.

## Character Management

The top section of the app contains character controls.

### Loading a Character

1. Select a character from the character dropdown.
2. Click **Load**.
3. The app reloads presets based on that character.
4. Roll history is cleared for the new active session.

### Creating a Character

1. Click **New**.
2. Fill out the character form.
3. Choose ability scores, proficiencies, advantages, and disadvantages.
4. Click **Save Character**.
5. The character is saved and can be loaded from the main window.

### Editing a Character

1. Select a character from the character dropdown.
2. Click **Edit**.
3. Update the character details.
4. Click **Save Character**.
5. The app refreshes character-based presets using the updated values.

The default character cannot be edited.

### Deleting a Character

1. Select a character from the character dropdown.
2. Click **Delete**.
3. Confirm the deletion.

The default character cannot be deleted.

## Project Structure

High-level project structure:
```text
dnd_dice_roller
- application
    - dice_roll_app_controller.py
- data
    - characters.json
    - presets.json
- domain
    - models
        - character.py
        - character_traits.py
        - dice.py
        - messages.py
        - roll.py
        - roll_history.py
    - services
        - character_service.py
        - dice_roll_service.py
        - preset_service.py
- storage
    - character_repository.py
    - preset_repository.py
- ui
    - character_window.py
    - character_window_layout.py
    - main_window.py
    - main_window_layout.py
    - ui_settings.py
- main.py
- README.md
- requirements.txt
```

## Architecture Overview

The app is split into a few simple layers:

### Models

Model classes represent the core application data and logic.

Examples:

- `Character`
- `Skills`
- `SavingThrows`
- `Roll`
- `RollHistory`
- `Die`

### Services

Service classes manage application behavior and business logic.

Examples:

- `CharacterService`
  - Loads characters
  - Creates characters
  - Updates characters
  - Deletes characters
  - Tracks the active character
  - Generates the next character ID
- `PresetService`
  - Loads presets
  - Saves presets
  - Adds character default presets
  - Manages custom presets
- `DiceRollService`
  - Handles dice rolling behavior

### Storage

Repository classes handle file persistence.

Examples:

- `CharacterRepository`
- `PresetRepository`

### UI

UI classes and layout files define the application windows and event handling.

Examples:

- `MainWindow`
- `CharacterWindow`
- `main_window_layout.py`
- `character_window_layout.py`

## Notes

- Character data is stored locally in `data/characters.json`.
- Presets are stored locally in `data/presets.json`.
- Character-based default presets are regenerated from the currently loaded character.
- Custom presets are user-managed.
- The default character exists as a safe startup fallback.