from typing import Optional
from Task import *
from utils import any
import json


class TaskList:
    """This class is used to store the list of courses that a student is taking."""

    def __init__(self):
        self.tasks: dict[str, Task] = self.__read_file()  # Task_name: Course

    def create_task(self, task: Task):
        """This method is used to add a course to the list."""
        if task.task_name in self.tasks:
            print(f"A Task with the name {task.task_name} already exists.")
            return
        self.tasks[task.task_name] = task
        self.__save_to_file()

    def get_tasks(self):
        """This method is used to get a course from the list."""
        return self.tasks.values()

    def get_task(self, task_name: str) -> Task:
        """
        This method is used to get a course from the list.
        Raises:
            Exception: If the course is not found in the list.
        Returns:
            Course: The course object.
        """
        if task_name in self.tasks:
            return self.tasks[task_name]
        else:
            # throw an exception
            raise Exception(f'No Task with the name "{task_name}" exists.')

    def delete_task(self, task_name: str, **kwarg):
        """This method is used to delete a course from the list."""
        if task_name in self.tasks:
            if kwarg.get("hard", False):
                # Hard delete
                del self.tasks[task_name]
            else:
                # Soft delete
                self.tasks[task_name].is_active = False
            self.__save_to_file()
        else:
            raise Exception("No such course exists in the list.")

    def spent_time(self, task_name: str, hours: int):
        """This method is used to add the time spent on a course."""
        if task_name in self.tasks:
            self.tasks[task_name].add_spent_time(hours)
            self.__save_to_file()
        else:
            raise Exception("No such course exists in the list.")

    def restore(self, task_name: str):
        """restore a task form the inactive state and make it active again."""
        if task_name in self.tasks:
            task : Task= self.tasks[task_name]
            if task.is_active:
                raise Exception("Task is already an active task")
            task.update(is_active=True)
            self.__save_to_file()
        else:
            raise Exception("No such course exists in the list.")


    def update_task(self, task_name_: str, **kwarg):
        """This method is used to update a course in the list."""
        print("update called ...")
        print(kwarg)
        if task_name_ in self.tasks:
            self.tasks[task_name_].update(**kwarg)
            updated_task = self.tasks[task_name_]
            # check if the course is renamed
            if task_name_ != updated_task.task_name:
                # delete the old task from the dictionary
                del self.tasks[task_name_]
                # add the new task to the dictionary by the new name
                self.tasks[updated_task.task_name] = updated_task

            self.__save_to_file()
        else:
            print("No such course exists in the list.")

    def display_list(self, **kwarg):
        """This method is used to display the list of courses."""
        active_status = kwarg.get("active")
        completed_status = kwarg.get("completed")
        short = kwarg.get("short", False)

        tasks = [ task
            for task in self.tasks.values()
            if task.is_active == active_status and
            task.is_completed() == completed_status
        ]

        if not tasks:
            raise Exception("No tasks to display.")

        for task in tasks:
            task.display(short=short)

    def __read_file(self) -> dict[str, Task]:
        """This method is used to read the tasks from the saved file."""
        try:
            with open("tasks.json", "r") as file:
                tasks = json.load(file)
                return {task: Task.fromJson(tasks[task]) for task in tasks}
        except Exception as e:
            print("! Error reading tasks from file.\n")
            print("__detail__")
            print(e)
            return {}

    def __save_to_file(self):
        """This method is used to save the tasks to the file."""
        try:
            with open("tasks.json", "w") as file:
                tasks = {
                    task: self.tasks[task].toJson() for task in self.tasks
                }
                json.dump(tasks, file)
        except:
            print("! Error saving tasks to file.")
