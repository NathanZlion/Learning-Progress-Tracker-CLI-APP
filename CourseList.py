from Course import *
import json


class CourseList:
    """This class is used to store the list of courses that a student is taking."""

    def __init__(self):
        self.courses: dict[str, Course] = self.__read_file()  # course_name: Course

    def create_course(self, course: Course):
        """This method is used to add a course to the list."""
        if course.course_name in self.courses:
            print("A course with the same name already exists.")
            return
        self.courses[course.course_name] = course
        self.__save_to_file()

    def get_courses(self):
        """This method is used to get a course from the list."""
        return self.courses.values()

    def delete_course(self, course_name: str, **kwarg):
        """This method is used to delete a course from the list."""
        if course_name in self.courses:
            if kwarg.get("hard", False):
                # Hard delete
                del self.courses[course_name]
            else:
                # Soft delete
                self.courses[course_name].is_active = False
            self.__save_to_file()
        else:
            print("No such course exists in the list.")

    def update_course(self, course_name: str, **kwarg):
        """This method is used to update a course in the list."""
        if course_name in self.courses:
            self.courses[course_name].update(**kwarg)
            updated_course = self.courses[course_name]
            # check if the course is renamed
            if course_name != updated_course.course_name:
                # delete the old course
                del self.courses[course_name]
                # add the new course
                self.courses[updated_course.course_name] = updated_course

            self.__save_to_file()
        else:
            print("No such course exists in the list.")

    def __read_file(self) -> dict[str, Course]:
        """This method is used to read the courses from the saved file."""
        try:
            with open("courses.json", "r") as file:
                courses = json.load(file)
                return {course: Course.fromJson(courses[course]) for course in courses}
        except:
            print("Error reading courses from file.")
            return {}

    def __save_to_file(self):
        """This method is used to save the courses to the file."""
        try:
            with open("courses.json", "w") as file:
                courses = {
                    course: self.courses[course].toJson() for course in self.courses
                }
                json.dump(courses, file)
        except:
            print("Error saving courses to file.")
