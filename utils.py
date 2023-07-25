import sys

# Utility methods
def get_input():
    """
    Get input from the user.
    """
    print("> ", end="")
    input = sys.stdin.readline()
    return input


class any:
    """
    A class that represents any type.
    """

    def __eq__(self, _):
        return True
