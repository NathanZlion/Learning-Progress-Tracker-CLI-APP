import sys

# Utility methods
def get_input():
    """
    Get input from the user.
    """
    user_input = input("> \b")
    return user_input.strip()


class any:
    """
    A class that represents any type.
    """

    def __eq__(self, _):
        return True
