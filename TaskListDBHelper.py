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
                    :task_name,
                    :task_spent_time,
                    :task_total_time,
                    :task_is_active,
                    :task_created_at
                )
                """,
                {
                    "task_name": task.task_name,
                    "task_spent_time": task.spent_time,
                    "task_total_time": task.total_time,
                    "task_is_active": 1 if task.is_active else 0,
                    "task_created_at": task.created_at,
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

        active_status = kwarg.get("active", any())
        completed_status = kwarg.get("completed", any())

        query_string = select_query_string(
            self.table_name, active_status=active_status, completed_status=completed_status
        )

        self.cursor.execute(query_string)
        tasks = self.cursor.fetchall()

        if not tasks:
            raise Exception("Error!: No tasks found.")
        
        return [Task.fromTuple(task) for task in tasks]


    def display_list(self, **kwarg) -> None:
        """This method is used to display the list of courses."""
        try:
            tasks = self.get_tasks(**kwarg)
            if not tasks:
                raise Exception("Error!: No tasks found.")

        except Exception as e:
            # just pass it up the stack. It will be handled by the caller.
            raise e

        short = kwarg.get("short", False)
        for task in tasks:
            task.display(short=short)

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
                SELECT * FROM {self.table_name} WHERE task_name = :task_name
                """,
                {"task_name": task_name},
            )
            task = self.cursor.fetchone()
            if task is None:
                raise Exception("Error!: No task by that name.")

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
                    DELETE FROM {self.table_name} WHERE task_name = :task_name
                    """,
                    {"task_name": task_name},
                )
            # soft delete: just make task inactive
            else:
                self.update_task(task_name, is_active=0)

            self.sqlite.commit()

        # exception where the task is not found in the list
        except Exception as e:
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
                task_name = :task_name,
                task_spent_time = :task_spent_time,
                task_total_time = :task_total_time,
                task_is_active = :task_is_active
                WHERE task_name = :task_name_
                """,
                {
                    "task_name": task.task_name,
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
            self.cursor.execute(
                f"""
                UPDATE {self.table_name} SET
                task_name = :task_name,
                task_spent_time = :task_spent_time,
                task_total_time = :task_total_time,
                task_is_active = :task_is_active
                WHERE task_name = :task_name_
                """,
                {
                    "task_name": kwarg.get("task_name", task_name_),
                    "task_spent_time": kwarg.get("spent_time", 0),
                    "task_total_time": kwarg.get("total_time", 0),
                    "task_is_active": kwarg.get("is_active", 1),
                    "task_name_": task_name_,
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
                task_name TEXT PRIMARY KEY,
                task_spent_time INTEGER,
                task_total_time INTEGER,
                task_is_active INTEGER,
                task_created_at
            )
            """
        )
        self.sqlite.commit()
    
    def close(self):
        """This method is used to save the changes to the database."""
        self.sqlite.commit() # save the changes to the database
        self.cursor.close()  # close the cursor
