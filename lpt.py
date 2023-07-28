import sys
import os
import time
from Task import Task
from utils import *
from TaskListDBHelper import TaskDb


class LPT:
    def __init__(self):
        self.tasksDb = TaskDb()

    def main(self):
        """Main function responsible for handling command line input processing
        and execution."""
        print_cli_welcome_message()
        while True:
            input: str = get_input()
            if input == "exit":
                self.tasksDb.close()
                clear_screen()
                print_exit_message()
                sys.exit(0)
            elif input == "clear":
                clear_screen()
                print_cli_header()
            else:
                self.process_and_execute_input(input)

    def process_and_execute_input(self, input: str):
        splitted_input = input.split()

        if not splitted_input:
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
        text = get_help_text(topic or "main")
        print(text)

    def add(self, *args):
        if not args or len(args[0]) < 2:
            self.help("add")
            return

        task_name, task_hours = args[0][0], args[0][1]
        try:
            self.tasksDb.create_task(Task(task_name, int(task_hours)))
        except Exception as e:
            print(e)

    def show(self, *args):
        if not args or len(args[0]) < 1:
            self.help("show")
            return

        task_name = args[0][0]
        try:
            task = self.tasksDb.get_task_by_name(task_name)
            task.display(short=True if "-s" in args[0] else False)
        except Exception as e:
            print(e)

    def list(self, *args):
        try:
            # default values
            active = True
            completed = False

            if "-all" in args[0] or "-a" in args[0]:
                active, completed = any(), any()
            
            if "-active" in args[0]:
                active = True
            
            elif "-inactive" in args[0]:
                active = False

            if "-completed" in args[0]:
                completed = True

            elif "-notcompleted" in args[0]:
                completed = False

            short = "-s" in args[0] or "-short" in args[0]
            self.tasksDb.display_list(active=active, completed=completed, short=short)

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
            self.tasksDb.update_task(task_name, **attributes)
        except Exception as e:
            print(e)

    def delete(self, *args):
        if not args or len(args[0]) < 1:
            self.help("delete")
            return

        task_name = args[0][0]
        try:
            self.tasksDb.delete_task(
                task_name, hard=("--hard" in args[0] or "-h" in args[0])
            )
        except Exception as e:
            print(e)

    def restore(self, *args):
        if not args or len(args[0]) < 1:
            self.help("restore")
            return

        task_name = args[0][0]

        try:
            self.tasksDb.restore(task_name)
        except Exception as e:
            print(e)

    # a command to add some hours spent on a task
    def spent(self, *args):
        if not args or len(args[0]) < 2:
            self.help("spent")
            return

        task_name, hours = args[0][0], args[0][1]
        try:
            self.tasksDb.spent_time(task_name, int(hours))
        except Exception as e:
            print(e)


if __name__ == "__main__":
    LPT().main()
