"""Module for displaying messages and results in the D&D Dice Roller 
application."""

from unittest import case
import random


class Messages:
    """Class to handle messages and results display in the application."""

    critical_fail_messages = [
        "Critical failure! Something went horribly wrong.",
        "Catastrophic failure! The worst possible outcome.",
        "Epic fail! This will have serious consequences."
    ]

    critical_success_messages = [
        "Critical success! Everything went right.",
        "Amazing success! The best possible outcome.",
        "Epic win! This will have fantastic consequences."
    ]

    poor_roll_messages = [
        "Poor roll! Better luck next time.",
        "Unfortunate outcome! Try again.",
        "Subpar result! Keep practicing."
    ]

    so_close_messages = [
        "So close! Just a bit more effort needed.",
        "Almost there! A tiny push could make it.",
        "So near yet so far! Keep trying."
    ]

    low_roll_messages = [
        "Low roll! Better luck next time.",
        "Unfortunate outcome! Try again.",
        "Subpar result! Keep practicing."
    ]

    mid_roll_messages = [
        "Mid roll! You're getting there.",
        "Decent outcome! Keep it up.",
        "Not bad! You're on the right track."
    ]

    good_roll_messages = [
        "Good roll! Well done.",
        "Nice outcome! Keep it up.",
        "Great job! You're on fire."
    ]

    @staticmethod
    def result_message(result):
        """Displays a message based on the result of a roll."""
        match result:
            case s if s == 1:
                return random.choice(Messages.critical_fail_messages)
            case s if 1 < s < 6:
                return random.choice(Messages.poor_roll_messages)
            case s if 6 <= s < 10:
                return random.choice(Messages.low_roll_messages)
            case s if 10 <= s < 15:
                return random.choice(Messages.mid_roll_messages)
            case s if 15 <= s < 19:
                return random.choice(Messages.good_roll_messages)
            case s if s == 19:
                return random.choice(Messages.so_close_messages)
            case s if s == 20:
                return random.choice(Messages.critical_success_messages)
            case _:
                return f"Roll Result: {result}"

    @staticmethod
    def update_roll_button_text(frame_variable):
        """
        Returns a context-specific label for a roll button based on the provided frame variable.

        Args:
            frame_variable (str): The type of roll context. Expected values are 
            "skill", "save", "weapon", or any other string.

        Returns:
            str: A label string appropriate for the given roll context.
                - "Show Your Skills!" for "skill"
                - "Hold Strong!" for "save"
                - "Bring the Pain!" for "weapon"
                - "Roll the Dice!" for any other value
        """
        match frame_variable:
            case "skill":
                return "Show Your Skills!"
            case "save":
                return "Hold Strong!"
            case "attack":
                return "Bring the Pain!"
            case _:
                return "Let's Roll!"
