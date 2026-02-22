# ui_settings.py
import FreeSimpleGUI as sg

class UISettings:
    """
    Provides global settings for the user interface, including font styles and
    methods to apply a consistent theme across the application.

    This class centralizes the configuration of GUI styles and ensures a uniform
    appearance across all elements. By utilizing the settings provided by this
    class, developers can define a cohesive look and feel for the application.

    :ivar normal_font: Default font specification for normal text.
    :type normal_font: tuple
    :ivar bold_font: Font specification for bold text.
    :type bold_font: tuple
    :ivar large_font: Font specification for large, bold text.
    :type large_font: tuple
    :ivar roll_result_font: Font specification for roll result text, typically
        large and bold to draw attention.
    :type roll_result_font: tuple
    """
    normal_font = ("Helvetica", 11)
    bold_font = ("Helvetica", 12, "bold")
    large_font = ("Helvetica", 16, "bold")
    roll_result_font = ("Helvetica", 18, "bold")

    @staticmethod
    def apply_theme():
        """
        Apply global GUI styling (theme + any global options).
        Call this once before constructing windows/elements.
        """
        sg.theme("DarkGrey15")

        sg.set_options(
            font=UISettings.normal_font
        )
