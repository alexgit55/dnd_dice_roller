"""Module for displaying messages and results in the D&D Dice Roller 
application."""

from unittest import case


class Messages:
    """Class to handle messages and results display in the application."""

    def __init__(self, master):
        self.master = master
        self.message_label = tk.Label(master, text="", bg="lightblue", font=("Arial", 12))
        self.message_label.pack()

    @staticmethod
    def display_message(message):
        """Displays a message in the message label."""
        Messages.message_label.config(text=message)

    @staticmethod
    def clear_message():
        """Clears the message label."""
        Messages.message_label.config(text="")

    @staticmethod
    def result_message(result):
        """Displays a message based on the result of a roll."""
        match result:
            case s if s == 1:
                return "What was that?!"
            case s if 1 < s < 6:
                return "Ouch that sucks!"
            case s if 6 <= s < 10:
                return "Eh still not great."
            case s if 10 <= s < 15:
                return "That's pretty good!"
            case s if 15 <= s < 20:
                return "Odds in your favor!"
            case s if s == 20:
                return "YES! Critical Success!"
            case _:
                return f"Roll Result: {result}"