from datetime import datetime


class Course:
    def __init__(
        self, course_name: str, course_number: int, credit_hours: float, **kwargs
    ):
        self.course_name: str = course_name
        self.course_number: int = course_number
        self.credit_hours = credit_hours
        self.hours_completed = kwargs.get("hours_completed", 0.0)
        self.is_active = kwargs.get("is_active", True)
        self.created_at: str = kwargs.get("created_at", datetime.now().isoformat())

    def is_complete(self) -> bool:
        return self.hours_completed >= self.credit_hours

    def toJson(self):
        return {
            "course_name": self.course_name,
            "course_number": self.course_number,
            "credit_hours": self.credit_hours,
            "hours_completed": self.hours_completed,
            "is_active": self.is_active,
            "created_at": self.created_at,
        }

    def update(self, **kwargs):
        self.course_name = kwargs.get("course_name", self.course_name)
        self.course_number = kwargs.get("course_number", self.course_number)
        self.credit_hours = kwargs.get("credit_hours", self.credit_hours)
        self.hours_completed = kwargs.get("hours_completed", self.hours_completed)
        self.is_active = kwargs.get("is_active", self.is_active)
        # Here it doesn't allow the user to change the created_at date 
        # because it is not a good practice to change the created_at date.

    @staticmethod
    def fromJson(json):
        course = Course(
            json["course_name"],
            json["course_number"],
            json["credit_hours"],
            hours_completed=json["hours_completed"],
            is_active=json["is_active"],
            created_at=json["created_at"],
        )
        return course

    def __repr__(self):
        return f"Course< {self.course_name} {self.course_number} {self.credit_hours} >"

    def __str__(self):
        return f"{self.course_name} {self.course_number} {self.credit_hours}"

    def __hash__(self):
        """Return a hash of the course name and number"""
        return hash(self.course_name + self.course_number)
