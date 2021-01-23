"""
Provides DescSearches, a collection of Course Calendar search functions.

Classes:

    DescSearches
"""


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
            semester (str): Either ['W', 'F', 'S', 'U'] semester codes.

        Raises:
            ValueError (Exception): If semester is not ['W', 'F', 'S', 'U'].

        Returns:
            (list): A list of courses in the passed semester
        """
        # TODO, I'd like to import the SemesterOffered Enum and use that here
        # for validation from !5.
        supportedCodes = ['W', 'F', 'S', 'U']
        returnCourses = []

        if semester not in supportedCodes:
            raise ValueError("semester not supported. Must be 'W', 'F', 'S'")

        for course in courses:
            if semester in course.semesters_offered:
                returnCourses.append(course)
        return returnCourses
