import sys
import os
import time
from Task import Task
from utils import *
from TaskList import TaskList


class LPT:
    def __init__(self):
        self.tasks = TaskList()

    def main(self):
        """
        Main function, called when script is run.
        """
        print("**************************************")
        print("     Welcome to the LPT CLI! __ where you track your tasks")
        print("**************************************")
        while True:
            input: str = get_input()
            if input == "exit\n":
                print("Exiting LPT ...")
                time.sleep(0.2)
                sys.exit(0)
            elif input == "clear\n":
                os.system("cls" if os.name == "nt" else "clear")
                print("Welcome to the LPT CLI!")
            else:
                self.process_input(input)

    def process_input(self, input: str):
        splitted_input = input.split()
        if len(splitted_input) == 0:
            return
        command = splitted_input[0]
        if command == "help":
            self.help(splitted_input[1] if len(splitted_input) > 1 else None)

        elif command == "add":
            self.add(splitted_input[1:])

        elif command == "show":
            self.show(splitted_input[1:])

        elif command == "list":
            self.list(splitted_input[1:])

        elif command == "edit":
            self.edit(splitted_input[1:])

        elif command == "delete":
            self.delete(splitted_input[1:])
        
        elif command == "restore":
            self.restore(splitted_input[1:])
        
        elif command == "spent":
            self.spent(splitted_input[1:])

        else:
            print(f'Command not found. Type "help" for a list of commands.')

    def help(self, topic: str | None = None):
        if not topic:
            print("This is the help telling...")
        else:
            print("This is the help telling you about {}".format(topic))

    def add(self, *args):
        if not args or len(args[0]) < 2:
            self.help("add")
            return

        task_name, task_hours = args[0][0], args[0][1]
        self.tasks.create_task(Task(task_name, int(task_hours)))

    def show(self, *args):
        if not args or len(args[0]) < 1:
            self.help("show")
            return

        task_name = args[0][0]
        try:
            task = self.tasks.get_task(task_name)
            task.display(short=True if "-s" in args[0] else False)
        except Exception as e:
            print(e)

    def list(self, *args):
        try:
            # show the active tasks only by default
            active = True
            if "-all" in args[0]:
                active = any()
            elif "-i" in args[0]:
                active = False

            completed = any()
            if "-c" in args[0]:
                completed = True
            elif "-nc" in args[0]:
                completed = False

            short = True if "-s" in args[0] else False
            self.tasks.display_list(active=active, completed=completed, short=short)

        except Exception as e:
            print(e)

    def edit(self, *args):
        if not args or len(args[0]) < 1:
            self.help("edit")
            return

        task_name = args[0][0]
        # Traverse through the. list of arguments to collect the attributes and values
        attributes = {}
        for i in range(1, len(args[0]), 2):
            attributes[args[0][i]] = args[0][i + 1]

        try:
            self.tasks.update_task(task_name, **attributes)
        except Exception as e:
            print(e)

    def delete(self, *args):
        if not args or len(args[0]) < 1:
            self.help("delete")
            return

        task_name = args[0][0]
        try:
            self.tasks.delete_task(task_name, hard="-hard" in args[0])
        except Exception as e:
            print(e)

    def restore(self, *args):
        if not args or len(args[0]) < 1:
            self.help("restore")
            return

        task_name = args[0][0]

        try:
            self.tasks.restore(task_name)
        except Exception as e:
            print(e)
    
    # a command to add some hours spent on a task
    def spent(self, *args):
        if not args or len(args[0]) < 2:
            self.help("spent")
            return

        task_name, hours = args[0][0], args[0][1]
        try:
            self.tasks.spent_time(task_name, int(hours))
        except Exception as e:
            print(e)

if __name__ == "__main__":
    LPT().main()
