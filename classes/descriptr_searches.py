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
