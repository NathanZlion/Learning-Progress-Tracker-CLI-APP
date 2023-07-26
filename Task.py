from datetime import datetime

class Task:
    def __init__(self, task_name: str, total_time: int, **kwargs):
        self.task_name: str = task_name
        self.total_time: int = total_time
        self.spent_time: int = kwargs.get("spent_time", 0)
        self.is_active : bool = kwargs.get("is_active", True)
        self.created_at: str = kwargs.get("created_at", datetime.now().isoformat())

    def is_completed(self) -> bool:
        try:
            return self.spent_time >= self.total_time
        except Exception as e:
            raise Exception("Cannot compare these two types, ", type(self.spent_time), type(self.
            total_time))

    def add_spent_time(self, hours: int):
        self.spent_time += hours

    def update(self, **kwargs):
        self.task_name = kwargs.get("task_name", self.task_name)
        self.total_time = kwargs.get("total_time", self.total_time)
        self.spent_time = kwargs.get("spent_time", self.spent_time)
        self.is_active = kwargs.get("is_active", self.is_active)
        # Here it doesn't allow the user to change the created_at date
        # because it is not a good practice to change the created_at date.

    def toJson(self):
        return {
            "task_name": self.task_name,
            "spent_time": self.spent_time,
            "total_time": int(self.total_time),
            "is_active": (self.is_active),
            "created_at": self.created_at,
        }
    
    @staticmethod
    def fromTuple(tuple):
        task_name = tuple[0]
        spent_time = tuple[1]
        total_time = tuple[2]
        is_active = bool(tuple[3])
        created_at = tuple[4]

        return Task(task_name, total_time, spent_time=spent_time, is_active=is_active, created_at=created_at)

    @staticmethod
    def fromJson(json):
        try:
            course = Task(
                json["task_name"],
                int(json["total_time"]),
                spent_time= int(json["spent_time"]),
                is_active=bool(json["is_active"]),
                created_at=json["created_at"],
            )
            return course

        except Exception as e:
            print(e)
            raise Exception("Error!: An error occurred while trying to read json task data. Invalid task json.")

    def __repr__(self):
        return f"Course< {self.task_name} {self.total_time} >"

    def __str__(self):
        return f"{self.task_name} {self.total_time}"

    def __hash__(self):
        """Return a hash of the course name and number"""
        return hash(self.task_name)

    def display(self, **kwargs):
        short = kwargs.get("short", False)
        progress = self.spent_time / self.total_time

        if short:
            print(f":: {self.task_name} :: {self.total_time}hrs :: ({progress * 100:.2f}% complete)")
        else:
            status = "Active" if self.is_active else "Inactive"
            separator_length = max(len(self.task_name), len(str(self.total_time)), len("Status: Inactive" if not self.is_active else "Status: Active"))

            print(f"""
  :: {self.task_name} :: {self.total_time}hrs :: Status: {status}
  :: {'-' * separator_length} :: {'-' * (len(str(self.total_time)) + 3)} :: {'-' * (len(status) + len("Status: "))}
  :: {self.spent_time}hrs/{self.total_time}hrs ({progress * 100:.2f}% complete)
  :: Date Created: {self.created_at}
  """)

