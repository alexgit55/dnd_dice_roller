# DnD Dice Roller

A lightweight desktop dice-rolling app for Dungeons & Dragons (and other TTRPGs) with a simple GUI.

## Features

- Roll common dice types (e.g., d20, d12, d10, d8, d6, d4)
- Roll multiple dice at once with an optional modifier
- d20 support for:
  - Normal rolls
  - Advantage
  - Disadvantage
- Roll history panel (click entries to reload)
- Presets:
  - Save current roll settings as a preset
  - Edit existing presets
  - Remove presets
- Presets are stored in `presets.json`

## Requirements

- Python 3.14+
- Dependencies listed in `requirements.txt`

## Setup (Windows/macOS/Linux)

Create and activate a virtual environment (recommended), then install dependencies.

### 1) Create a virtual environment
   ```bash
   python -m venv .venv
   ```

### 2) Activate it

**Windows (PowerShell):**
   ```bash
   .venv\Scripts\Activate.ps1
   ```

**Windows (cmd):**
   ```cmd
   .venv\Scripts\Activate
   ```

**macOS/Linux:**
   ```bash
   source .venv/bin/activate
   ```

### 3) Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

## Run the app

From the project directory:
   ```bash
   python main.py
   ```

## Project Structure (high level)

- `main.py` — GUI application entry point
- `dice.py` — dice and rolling logic
- `roll.py` — roll/preset/history management
- `messages.py` — roll result messaging
- `presets.json` — saved presets (created/updated by the app)
- `requirements.txt` — pinned dependencies

## Notes

- Presets and history behavior depend on local files; commit `presets.json` only if you want to share default presets with others.
