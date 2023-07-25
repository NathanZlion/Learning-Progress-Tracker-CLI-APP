import sys
import os
import time
from utils import *

from CourseList import CourseList


class LPT:
    def __init__(self):
        self.courses = CourseList()

    def main(self):
        """
        Main function, called when script is run.
        """
        print("Welcome to the LPT CLI!")
        while True:
            input: str = get_input()
            if input == "exit\n":
                print("Exiting LPT ...")
                time.sleep(1)
                sys.exit(0)
            elif input == "clear\n":
                os.system("cls" if os.name == "nt" else "clear")
                print("Welcome to the LPT CLI!")
            else:
                self.process_input(input)

    def process_input(self, input: str):
        print("other input")


if __name__ == "__main__":
    LPT().main()
