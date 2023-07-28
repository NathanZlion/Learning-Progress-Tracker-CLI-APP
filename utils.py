import os
from HelpText import *
import time


# Utility methods
def get_input():
    """
    Get input from the user.
    """
    user_input = input(">  \b")
    return user_input.strip()


class any:
    """A class that represents any type."""

    def __eq__(self, _):
        return True


def is_any(value):
    """Check if a value is of type any."""
    return isinstance(value, any)


def select_query_string(
    table_name: str,
    active_status: bool | any = any(),
    completed_status: bool | any = any(),
) -> str:
    """
    Generate a select query string for task selection.
    """

    if is_any(active_status) and is_any(completed_status):
        return f"SELECT * FROM {table_name}"

    elif not is_any(active_status) and is_any(completed_status):
        return f"SELECT * FROM {table_name} WHERE is_active = {1 if active_status else 0}"

    elif is_any(active_status) and not is_any(completed_status):
        # Query for selecting tasks with spent_time not 0 and greater than or equal to total_time if completed_status is True else less than total_time
        if completed_status:
            return f"SELECT * FROM {table_name} WHERE spent_time > 0 AND spent_time >= total_time"
        else:
            return f"SELECT * FROM {table_name} WHERE spent_time > 0 AND spent_time < total_time"

    else:
        # Query for selecting tasks based on both active and completed status
        if completed_status:
            return f"SELECT * FROM {table_name} WHERE is_active = {1 if active_status else 0} AND spent_time > 0 AND spent_time < total_time"
        else:
            return f"SELECT * FROM {table_name} WHERE is_active = {1 if active_status else 0} AND spent_time > 0 AND spent_time >= total_time"


def print_cli_welcome_message():
    print("*" * 15)
    print("     Welcome to the LPT CLI! __ where you track your tasks")
    print("*" * 15)


def print_cli_header():
    print("*" * 10)
    print("     LPT CLI __")
    print("*" * 10)


def get_help_text(topic):
    return help_text.get(
        topic, f'Help topic "{topic}" not found. Type "help" for a list of commands.'
    )


def print_exit_message():
    """prints a cool animation while exiting LPT CLI"""
    animation_chars = ["|", "/", "-", "\\"]
    num_chars = len(animation_chars)

    for _ in range(
        2
    ):  # Adjust the number of iterations for a longer or shorter animation
        for i in range(num_chars):
            print(f"\rExiting LPT CLI... {animation_chars[i]}", end="")
            time.sleep(0.1)  # Adjust the sleep duration to control the animation speed

    print("   BYE BYE! Stay Productive.\n")  # Add a newline after the animation is done


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
