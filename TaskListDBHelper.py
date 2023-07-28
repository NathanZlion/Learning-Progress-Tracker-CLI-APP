from Task import *
import sqlite3
from utils import *


class TaskDb:
    """This class is used to store the list of courses that a student is taking."""

    def __init__(self):
        """Initialize the list of courses."""
        self.table_name = "tasks"
        self.sqlite = sqlite3.connect("database.db")
        self.cursor : sqlite3.Cursor = self.sqlite.cursor()
        self.__create_table()


    def create_task(self, task: Task):
        """This method is used to add a course to the list."""
        try:
            self.cursor.execute(
                f"""
                INSERT INTO {self.table_name} VALUES (
                    :name,
                    :spent_time,
                    :total_time,
                    :is_active,
                    :created_at
                )
                """,
                {
                    "name": task.name,
                    "spent_time": task.spent_time,
                    "total_time": task.total_time,
                    "is_active": 1 if task.is_active else 0,
                    "created_at": task.created_at,
                },
            )
            self.sqlite.commit()

        except sqlite3.IntegrityError as e:
            raise Exception("Error!: A task with the same name already exists.")

        except Exception as e:
            raise e

    def get_tasks(self, **kwarg) -> list[Task]:
        """This method is used to get tasks from the list.
        If no arguments are passed, it will return all the tasks.
        - If the argument "active" is passed, it will return all the active or non 
        active tasks based on the value of the argument.
        - If the argument "completed" is passed, it will return all the completed or
        non completed tasks based on the value of the argument.

        Raises:
            Exception: If no tasks are found in the list.
        Returns:
            list[Task]: The list of tasks.
        """
        active = kwarg.get("active", any())
        completed = kwarg.get("completed", any())

        query_string = select_query_string(
            self.table_name, active_status=active, completed_status=completed
        )

        self.cursor.execute(query_string)
        tasks = self.cursor.fetchall()

        if not tasks:
            raise Exception("⣿ No tasks found.\n")
        try:
            return [Task.fromTuple(task) for task in tasks]
        
        except Exception as e:
            raise e


    def display_list(self, **kwarg) -> None:
        """This method is used to display the list of courses."""
        try:
            tasks = self.get_tasks(**kwarg)
            if not tasks:
                raise Exception("⣿ No tasks found.\n")

            short = kwarg.get("short", False)
            print (f"⣿ Tasks: {len(tasks)} tasks found.")
            for index, task in enumerate(tasks):
                print_separator()
                print(f'{index+1}',end=". ")
                print(task.get_display_string(short=short), end="\n")
            print("\n")

        except Exception as e:
            # just pass it up the stack. It will be handled by the caller.
            raise e


    def get_task_by_name(self, task_name: str) -> Task:
        """
        This method is used to get a task from the list.
        Raises:
            Exception: If the task is not found in the list.
        Returns:
            Task: The task object.
        """
        try:
            self.cursor.execute(
                # select one task from the database
                f"""
                SELECT * FROM {self.table_name} WHERE name = :task_name
                """,
                {"task_name": task_name},
            )
            task = self.cursor.fetchone()
            if task is None:
                raise Exception("⣿ No task by that name found.\n")

            return Task.fromTuple(task)

        except sqlite3.IntegrityError:
            raise Exception("Error!: A task with the same name already exists.")
        


    def delete_task(self, task_name: str, **kwarg):
        """This method is used to delete a course from the list.
        
        Raises:
            Exception: If the task by the name `task_name` is not found in the list.
        """
        try:
            # hard delete: delete the task from the database
            if kwarg.get("hard", False):
                self.cursor.execute(
                    f"""
                    DELETE FROM {self.table_name} WHERE name = :task_name
                    """,
                    {"task_name": task_name},
                )
            # soft delete: just make task inactive
            else:
                self.update_task(task_name, is_active=0)

            self.sqlite.commit()

        # exception where the task is not found in the list
        except Exception as e:
            error_message = f"Error!: No task by the name {task_name} found. ,{e.__class__.__name__}"
            raise e

    def spent_time(self, task_name: str, hours: int):
        """This method is used to add the time spent on a course.
        
        Raises:
            Exception: If the task by the name `task_name` is not found in the list.
        """

        try:
            task = self.get_task_by_name(task_name)
            task.spent_time += hours
            self.cursor.execute(
                f"""
                UPDATE {self.table_name} SET
                name = :task_name,
                spent_time = :task_spent_time,
                total_time = :task_total_time,
                is_active = :task_is_active
                WHERE name = :task_name_
                """,
                {
                    "task_name": task.name,
                    "task_spent_time": task.spent_time,
                    "task_total_time": task.total_time,
                    "task_is_active": 1 if task.is_active else 0,
                    "task_name_": task_name,
                },
            )

            self.sqlite.commit()

        except Exception as e:
            raise e


    def restore(self, task_name: str) -> None:
        """restore a task form the inactive state and make it active again.

        Raises:
            Exception: If the task by the name `task_name` is not found in the list.
        """
        try:
            task = self.get_task_by_name(task_name)
            task.is_active = True
            self.update_task(task_name, is_active=1)

        except Exception as e:
            raise e


    def update_task(self, task_name_: str, **kwarg) -> None:
        """This method is used to update a task in the list.

        Raises:
            Exception: If the task is not found in the list.
        """
        try:
            existing_task = self.get_task_by_name(task_name_)
            if not existing_task:
                raise Exception("⣿ No such tasks found.")

            self.cursor.execute(
                f"""
                UPDATE {self.table_name} SET
                name = :task_name,
                spent_time = :task_spent_time,
                total_time = :task_total_time,
                is_active = :task_is_active
                WHERE name = :task_name_
                """,
                {
                    "task_name": kwarg.get("task_name", existing_task.name),
                    "task_spent_time": kwarg.get("spent_time", existing_task.spent_time),
                    "task_total_time": kwarg.get("total_time", existing_task.total_time),
                    "task_is_active": kwarg.get("is_active", existing_task.is_active),
                    "task_name_": existing_task.name,
                },
            )
            self.sqlite.commit()
        except sqlite3.IntegrityError as e:
            raise Exception("Error!: A task with the same name already exists.")


    def __create_table(self):
        """This method is used to create the table of tasks if it doesn't exist already."""
        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                name TEXT PRIMARY KEY,
                spent_time INTEGER,
                total_time INTEGER,
                is_active INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.sqlite.commit()
    
    def close(self):
        """This method is used to save the changes to the database."""
        self.sqlite.commit() # save the changes to the database
        self.cursor.close()  # close the cursor
