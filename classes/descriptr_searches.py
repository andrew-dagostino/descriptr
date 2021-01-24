"""
Provides DescSearches, a collection of Course Calendar search functions.

Classes:

    DescSearches
"""

from classes.course_enums import SemesterOffered


class DescSearches:
    """
    A collection of search functions.

    Methods:
        bySemester(courses, semester):
            Search courses by semester.
    """

    def bySemester(self, courses, semester):
        """
        Filter the passed array of courses by passed semester.

        Args:
            courses (list<Course>): An array of Course data structures.
            semester (Enum SemesterOffered): A supported semester code.

        Raises:
            ValueError (Exception): If semester is not in SemesterOffered Enum.

        Returns:
            (list): A list of courses in the passed semester
        """
        returnCourses = []

        if not isinstance(semester, SemesterOffered):
            raise ValueError("Code not supported. Not in SemesterOffered enum")

        for course in courses:
            if semester in course.semesters_offered:
                returnCourses.append(course)
        return returnCourses

    def byCourseCode(self, courses, code):
        """
        Filter the passed array of courses by passed course code (eg. ACCT, CIS).

        Args:
            courses (List<Course>): An array of Course data structures.
            code (String): The letter portion of a course's id (eg. CIS, ECON)

        Returns:
            (list): A list of courses with the supplied course code
        """

        returnCourses = []

        for course in courses:
            if course.code.lower() == code.lower():
                returnCourses.append(course)

        return returnCourses

    def byCourseLevel(self, courses, level):
        """
        Filter the passed array of courses by passed course level

        Args:
            courses (List<Course>): An array of Course data structures.
            level (Integer): The leading digit of the course number

        Raises:
            ValueError (Exception): If level is not an integer between 1 and 9

        Returns:
            (list): A list of courses with course numbers starting with the passed digit
        """

        returnCourses = []

        if not isinstance(level, Integer):
            raise ValueError("Course level must be an integer")

        if level < 1 or level > 9:
            raise ValueError("Course level has invalid range")

        for course in courses:
            if str(course.number).startsWith(str(level)):
                returnCourses.append(course)

        return returnCourses

    def byCourseNumber(self, courses, number):
        """
        Filter the passed array of courses by passed course number (eg. 1250, 4720).

        Args:
            courses (List<Course>): An array of Course data structures.
            number (Integer): The 4-digit number of a course

        Raises:
            ValueError (Exception): If number is not a 4-digit integer

        Returns:
            (list): A list of courses with matching course numbers
        """

        returnCourses = []

        if not isinstance(number, Integer):
            raise ValueError("Course number must be an integer")

        if number < 1000 or number > 9999:
            raise ValueError("Course number has invalid range")

        for course in courses:
            if course.number == number:
                returnCourses.append(course)

        return returnCourses
