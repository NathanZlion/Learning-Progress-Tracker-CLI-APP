from datetime import datetime

class Task:
    def __init__(self, task_name: str, task_hours: int, **kwargs):
        self.task_name: str = task_name
        self.task_hours: int = task_hours
        self.hours_spent: int = kwargs.get("hours_spent", 0)
        self.is_active : bool = kwargs.get("is_active", True)
        self.created_at: str = kwargs.get("created_at", datetime.now().isoformat())

    def is_completed(self) -> bool:
        try:
            return self.hours_spent >= self.task_hours
        except Exception as e:
            print(type(self.hours_spent))
            print(type(self.task_hours))
            raise Exception("Cannot compare these two types, ", type(self.hours_spent), type(self.
            task_hours))

    def add_spent_time(self, hours: int):
        self.hours_spent += hours

    def update(self, **kwargs):
        self.task_name = kwargs.get("task_name", self.task_name)
        self.task_hours = kwargs.get("task_hours", self.task_hours)
        self.hours_spent = kwargs.get("hours_spent", self.hours_spent)
        self.is_active = kwargs.get("is_active", self.is_active)
        # Here it doesn't allow the user to change the created_at date
        # because it is not a good practice to change the created_at date.

    def toJson(self):
        return {
            "task_name": self.task_name,
            "task_hours": int(self.task_hours),
            "hours_spent": self.hours_spent,
            "is_active": self.is_active,
            "created_at": self.created_at,
        }

    @staticmethod
    def fromJson(json):
        try:
            course = Task(
                json["task_name"],
                int(json["task_hours"]),
                hours_spent= int(json["hours_spent"]),
                is_active=bool(json["is_active"]),
                created_at=json["created_at"],
            )
            return course

        except Exception as e:
            raise Exception("Error!: An error occurred while trying to read json task data. Invalid task json.")

    def __repr__(self):
        return f"Course< {self.task_name} {self.task_hours} >"

    def __str__(self):
        return f"{self.task_name} {self.task_hours}"

    def __hash__(self):
        """Return a hash of the course name and number"""
        return hash(self.task_name)

    def display(self, **kwargs):
        short = kwargs.get("short", False)
        progress = self.hours_spent / self.task_hours

        if short:
            print(f":: {self.task_name} :: {self.task_hours}hrs :: ({progress * 100:.2f}% complete)")
        else:
            status = "Active" if self.is_active else "Inactive"
            separator_length = max(len(self.task_name), len(str(self.task_hours)), len("Status: Inactive" if not self.is_active else "Status: Active"))

            print(f"""
  :: {self.task_name} :: {self.task_hours}hrs :: Status: {status}
  :: {'-' * separator_length} :: {'-' * (len(str(self.task_hours)) + 3)} :: {'-' * (len(status) + len("Status: "))}
  :: {self.hours_spent}hrs/{self.task_hours}hrs ({progress * 100:.2f}% complete)
  :: Date Created: {self.created_at}
  """)

