"""Module for displaying messages and results in the D&D Dice Roller 
application."""

import os

from dotenv import load_dotenv

from google import genai
from google.genai import types

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api_key)

class Messages:
    """Class to handle messages and results display in the application."""

    @staticmethod
    def result_message(result):
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
        response = ""
        match result:
            case s if s == 1:
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents="Write a quick one sentence miserable reaction to rolling a 1 on a d20.",
                    config=types.GenerateContentConfig(
                        thinking_config=types.ThinkingConfig(thinking_level="minimal"))
                )
            case s if 1 < s < 10:
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents="Write a quick one sentence sad reaction to rolling low on d20.",
                    config=types.GenerateContentConfig(
                        thinking_config=types.ThinkingConfig(thinking_level="minimal"))
                )
            case s if 10 <= s < 15:
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents="Write a quick one sentence neutral reaction to rolling above average on a d20.",
                    config=types.GenerateContentConfig(
                        thinking_config=types.ThinkingConfig(thinking_level="minimal"))
                )
            case s if 15 <= s < 20:
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents="Write a quick one sentence happy reaction to getting a high roll on a d20.",
                    config=types.GenerateContentConfig(
                        thinking_config=types.ThinkingConfig(thinking_level="minimal"))
                )
            case s if s == 20:
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents="Write a quick one sentence excited reaction to rolling a 20 on a d20.",
                    config=types.GenerateContentConfig(
                        thinking_config=types.ThinkingConfig(thinking_level="minimal"))
                )
            case _:
                response = f"Roll Result: {result}"

        return response.text

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