"""Module for displaying messages and results in the D&D Dice Roller 
application."""

from unittest import case


class Messages:
    """Class to handle messages and results display in the application."""

    @staticmethod
    def result_message(result):
        """Displays a message based on the result of a roll."""
        match result:
            case s if s == 1:
                return "What was that?!"
            case s if 1 < s < 6:
                return "Ouch that sucks!"
            case s if 6 <= s < 10:
                return "Eh not that great."
            case s if 10 <= s < 15:
                return "That's pretty good!"
            case s if 15 <= s < 19:
                return "Odds in your favor!"
            case s if s == 19:
                return "AHH So close to a Critical!"
            case s if s == 20:
                return "YES! Critical Success!"
            case _:
                return f"Roll Result: {result}"
