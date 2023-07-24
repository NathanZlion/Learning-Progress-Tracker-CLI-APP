from Course import *
from typing import Dict, List

import json


class CourseList:
    """This class is used to store the list of courses that a student is taking."""

    def __init__(self):
        self.courses : Dict[str, Course]= {}

    def create_course(self, course: Course):
        """This method is used to add a course to the list."""
        self.courses[course] = course
        self.__save_to_file()

    def delete_course(self, course_name: str, **kwarg):
        """This method is used to delete a course from the list."""
        if course_name in self.courses:
            if kwarg.get("hard", False):
                del self.courses[course_name]
            else:
                self.courses[course_name].is_active = False
            self.__save_to_file()
        else:
            print("No such course exists in the list.")

    def update_course(self, course_name: str, **kwarg):
        """This method is used to update a course in the list."""
        if course_name in self.courses:
            self.courses[course_name].update(**kwarg)
            self.__save_to_file()
        else:
            print("No such course exists in the list.")


    def get_courses(self) -> List[Course]:
        """This method is used to get a course from the list."""
        return list(self.courses.values())

    def __read_file(self) -> dict[str, Course]:
        """This method is used to read the courses from the saved file."""
        try:
            with open("courses.json", "r") as f:
                courses = json.load(f)
                return {course: Course.fromJson(courses[course]) for course in courses}
        except:
            print("Error reading courses from file.")
            return {}

    def __save_to_file(self):
        """This method is used to save the courses to the file."""
        try:
            with open("courses.json", "w") as f:
                courses = {
                    course: self.courses[course].toJson() for course in self.courses
                }
                json.dump(courses, f)
        except:
            print("Error saving courses to file.")
