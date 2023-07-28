from datetime import datetime


class Task:
    def __init__(self, task_name: str, total_time: int, **kwargs):
        self.name: str = task_name
        self.total_time: int = total_time
        self.spent_time: int = kwargs.get("spent_time", 0)
        self.is_active: bool = kwargs.get("is_active", True)
        self.created_at: str = kwargs.get("created_at", datetime.now().isoformat())

    def is_completed(self) -> bool:
        try:
            return self.spent_time >= self.total_time
        except Exception as e:
            error_message = f"Error!: An error occurred while trying to check if \
                the task is completed. {e.__class__.__name__}"
            raise Exception(error_message)

    def add_spent_time(self, hours: int):
        self.spent_time += hours

    def update(self, **kwargs):
        self.name = kwargs.get("name", self.name)
        self.total_time = kwargs.get("total_time", self.total_time)
        self.spent_time = kwargs.get("spent_time", self.spent_time)
        self.is_active = kwargs.get("is_active", self.is_active)
        # Here it doesn't allow the user to change the created_at date
        # because it is not a good practice to change the created_at date.

    def toJson(self):
        return {
            "name": self.name,
            "spent_time": self.spent_time,
            "total_time": int(self.total_time),
            "is_active": (self.is_active),
            "created_at": self.created_at,
        }

    @staticmethod
    def fromTuple(tuple_task) -> "Task":
        name, spent_time, total_time, is_active, created_at = tuple_task
        return Task(
            name,
            total_time,
            spent_time=spent_time,
            is_active=is_active,
            created_at=created_at,
        )

    def __repr__(self):
        return f"Course< {self.name} {self.total_time} >"

    def __str__(self):
        return f"{self.name} {self.total_time}"

    def __hash__(self):
        """Return a hash of the course name and number"""
        return hash(self.name)

    def display(self, **kwargs):
        short = kwargs.get("short", False)
        try:
            progress = self.spent_time / self.total_time
            if short:
                print(
                    f":: {self.name} :: {self.total_time}hrs :: ({progress * 100:.2f}% complete)"
                )
            else:
                status = "Active" if self.is_active else "Inactive"
                separator_length = max(
                    len(self.name),
                    len(str(self.total_time)),
                    len("Status: Inactive" if not self.is_active else "Status: Active"),
                )

                print(
                f"""
  :: {self.name} :: {self.total_time}hrs :: Status: {status}
  :: {'-' * separator_length} :: {'-' * (len(str(self.total_time)) + 3)} :: {'-' * (len(status) + len("Status: "))}
  :: {self.spent_time}hrs/{self.total_time}hrs ({progress * 100:.2f}% complete)
  :: Date Created: {self.created_at}
  """
            )
        except ZeroDivisionError:
            progress = 0
            print("Hige Dick")

        except Exception as e:
            print("Dick head")