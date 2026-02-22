"""Module for displaying messages and results in the D&D Dice Roller 
application."""

import os

from dotenv import load_dotenv

from google import genai
from google.genai import types

class Messages:
    """
    Encapsulates functionalities for handling structured messaging tasks.

    This class is responsible for generating and managing messages tied to specific inputs,
    like a d20 roll result. It utilizes a content generation model for dynamic and contextually
    appropriate responses.

    :ivar gemini_api_key: API key for authentication with the content generation model.
    :type gemini_api_key: str
    :ivar client: Client object for interacting with the content generation model.
    :type client: genai.Client
    """
    def __init__(self):
        load_dotenv()
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.gemini_api_key)
        self.model = "gemini-2.5-flash"

    def result_message(self, result):
        """
        Generate a message based on the result of a d20 roll.

        This method generates and returns a message corresponding to the provided result
        of a d20 roll. The message is dynamically generated through a content generation
        model, and it reflects the mood or reaction appropriate for the given roll result.

        :param result: The numerical outcome of the d20 roll.
        :type result: int
        :return: A string message reflecting the mood or reaction based on the roll result.
        :rtype: str
        """
        result_text = ""
        match result:
            case s if s == 1:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents="Write a quick one sentence miserable reaction to getting a critical failure on a d20."
                )
                result_text = response.text
            case s if 2 < s < 10:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents="Write a quick one sentence sad reaction to rolling low but above a critical failure on d20."
                )
                result_text = response.text
            case s if 10 <= s < 15:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents="Write a quick one sentence neutral reaction to rolling above average on a d20."
                )
                result_text = response.text
            case s if 15 <= s < 20:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents="Write a quick one sentence happy reaction to getting a high roll on a d20."
                )
                result_text = response.text
            case s if s == 20:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents="Write a quick one sentence excited reaction getting a critical success on a d20."
                )
                result_text = response.text
            case _:
                result_text = f"Roll Result: {result}"

        return result_text

if __name__ == "__main__":
    load_dotenv()
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_api_key)

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents="Write a quick excited reaction to rolling a 20 on a d20.",
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_level="low"))
    )
    print(response.text)