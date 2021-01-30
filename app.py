#!/usr/bin/env python3

import sys
import re

"""
Provides Descriptr, a subclass of cmd.

A set of commands for searching UofG Course Calendars.

Classes:

    Descriptr
"""

import cmd
from classes.course_enums import SemesterOffered
from classes.course_parser import CourseParser
from classes.descriptr_searches import DescSearches
from classes.pdf_converter import PDFConverter


class Descriptr(cmd.Cmd):
    """
    Represents a Read-Eval-Print Loop that interacts with the course calendar.

    Methods:
        do_exit():
            Exit Descriptr.
        do_search_code(args):
            Search by course code.
        do_search_department(args):
            Search by department.
        do_search_keyword(args):
            Search by keyword.
        do_search_level(args):
            Search by course level.
        do_search_number(args):
            Search by exact course number.
        do_search_semester(args):
            Search by semester.
        do_search_weight(args):
            Search by credit weight.
    """

    intro = ("This is Descriptr.\n"
             "Search for courses in the 2020-2021 UofG Course Calendar.\n"
             "Type help or ? to list commands.\n"
             "Type 'help <command>' for in command-specific help.\n"
             )
    prompt = "desc >> "

    def __init__(self):  # {{{
        """Use PDFConverter to convert Course Cal to text. Init cmd loop."""
        filepath = 'c12.pdf'
        if len(sys.argv) > 1:
            for i in range(1, len(sys.argv)):
                if(re.match(".+\\.pdf", sys.argv[i])):
                    filepath = sys.argv[i]
                    break

        self._load(filepath)

        super().__init__()  # Call to cmd Object's init
        # }}}

    def _load(self, filepath):
        converter = PDFConverter()
        parser = CourseParser()

        print("Converting...")
        converter.openPDF(filepath)

        print("Parsing...")
        self.all_courses = parser.open_file("converted-pdf.txt")

        print("Loading Complete")
        self.carryover_data = []  # A copy of data returned from search here.
        self.search = DescSearches()

    def do_exit(self, args):  # {{{
        """
        Exit Descriptr.

            Usage:
                exit
        """
        exit(0)
        # }}}

    def do_load_pdf(self, args):
        """
        Parse and load a new courses PDF

            Usage: load_pdf <filepath>

                <filepath> : The filepath to the PDF file to load
        """

        args = args.split(' ')
        if args[0] == '':
            print("[E] Please provide an argument")
            print(self.do_search_code.__doc__)
            return

        # Find the first pdf file
        filepath = None
        for arg in args:
            if(re.match(".+\\.pdf", arg, re.IGNORECASE)):
                filepath = arg
                break

        if filepath is None:
            print("[E] Provided file must be a PDF")
            print(self.do_load_pdf.__doc__)
            return
        else:
            self._load(filepath)

    def do_search_code(self, args):  # {{{
        """
        Search by course code.

        Usage: search_code <course_code> [-n]

            <course_code> : The course letters e.g. CIS
            -n            : Optional. If passed, will search the output of the previous search.
                            Otherwise, searches the whole course calendar.
        """
        search_array = self.all_courses
        code = ''
        args = args.split(' ')

        if args[0] == '':
            print("[E] Please provide an argument")
            print(self.do_search_code.__doc__)
            return

        # Check for -n, if there is carryover_data, search it instead of all_courses
        for arg in args:
            if arg == "-n":
                if self.carryover_data:
                    search_array = self.carryover_data

        # Find the first code
        for arg in args:
            if arg[0] != '-':
                code = arg
                break

        results = self.search.byCourseCode(search_array, code)

        if results:
            self.carryover_data = results
            print("\n")
            for course in results:
                print(course)
            print(f"Matched {len(results)}")
        else:
            print(f" No courses match code '{code}'")
        # }}}

    def do_search_department(self, args):  # {{{
        """
        Search by department.

        Usage: search_department <department> [-n]

            <department> : The department e.g. Department of Clinical Studies
            -n           : Optional. If passed, will search the output of the previous search.
                            Otherwise, searches the whole course calendar.
        """
        search_array = self.all_courses
        args = args.split(' ')

        if args[0] == '':
            print("[E] Please provide an argument")
            print(self.do_search_department.__doc__)
            return

        # Check for -n, if there is carryover_data, search it instead of all_courses
        # also remove it from the args
        for arg in args:
            if arg == "-n":
                if self.carryover_data:
                    search_array = self.carryover_data
                index = args.index(arg)
                args.pop(index)
                break

        # Re-attach the args into a string
        department = " ".join(args)

        results = self.search.byDepartment(search_array, department)

        if results:
            self.carryover_data = results
            print("\n")
            for course in results:
                print(course)
            print(f"Matched {len(results)}")
        else:
            print(f" No courses match department '{department}'")
        # }}}

    def do_search_keyword(self, args):  # {{{
        """
        Search by keyword.

        Usage: search_keyword <keyword> [-n]

            <keyword> : The term to search e.g. biology
            -n        : Optional. If passed, will search the output of the previous search.
                        Otherwise, searches the whole course calendar.
        """
        search_array = self.all_courses
        key = ''
        args = args.split(' ')

        if args[0] == '':
            print("[E] Please provide an argument")
            print(self.do_search_keyword.__doc__)
            return

        # Check for -n, if there is carryover_data, search it instead of all_courses
        for arg in args:
            if arg == "-n":
                if self.carryover_data:
                    search_array = self.carryover_data

        # Find the first code
        for arg in args:
            if arg[0] != '-':
                key = arg
                break

        try:
            results = self.search.byKeyword(search_array, key)

            if results:
                self.carryover_data = results
                print("\n")
                for course in results:
                    print(course)
                print(f"Matched {len(results)}")
            else:
                print(f" No courses contain keyword '{key}'")
        except ValueError as e:
            print(f"[E]: {e}")

        # }}}

    def do_search_level(self, args):  # {{{
        """
        Search by course level.

        Usage: search_level <course_level> [-n]

            <course_level> : The leading number of a course number e.g. 3
            -n            : Optional. If passed, will search the output of the previous search.
                            Otherwise, searches the whole course calendar.
        """
        search_array = self.all_courses
        level = ''
        args = args.split(' ')

        if args[0] == '':
            print("[E] Please provide an argument")
            print(self.do_search_level.__doc__)
            return

        # Check for -n, if there is carryover_data, search it instead of all_courses
        for arg in args:
            if arg == "-n":
                if self.carryover_data:
                    search_array = self.carryover_data

        # Find the first code
        for arg in args:
            if arg[0] != '-':
                level = arg
                break

        try:
            results = self.search.byCourseLevel(search_array, level)

            if results:
                self.carryover_data = results
                print("\n")
                for course in results:
                    print(course)
                print(f"Matched {len(results)}")
            else:
                print(f" No courses match level '{level}'")
        except ValueError as e:
            print(f"[E]: {e}")
        # }}}

    def do_search_number(self, args):  # {{{
        """
        Search by full course number, not just course level.

        Usage: search_number <course_number> [-n]

            <course_number> : The full number of a course e.g. 2750
            -n              : Optional. If passed, will search the output of the previous search.
                                Otherwise, searches the whole course calendar.
        """
        search_array = self.all_courses
        num = ''
        args = args.split(' ')

        if args[0] == '':
            print("[E] Please provide an argument")
            print(self.do_search_number.__doc__)
            return

        # Check for -n, if there is carryover_data, search it instead of all_courses
        for arg in args:
            if arg == "-n":
                if self.carryover_data:
                    search_array = self.carryover_data

        # Find the first code
        for arg in args:
            if arg[0] != '-':
                num = arg
                break

        try:
            results = self.search.byCourseNumber(search_array, num)

            if results:
                self.carryover_data = results
                print("\n")
                for course in results:
                    print(course)
                print(f"Matched {len(results)}")
            else:
                print(f" No courses match number '{num}'")
        except ValueError as e:
            print(f"[E]: {e}")
        # }}}

    def do_search_semester(self, args):  # {{{
        """
        Search by semester.

        Usage: search_semester <semester_code> [-n]

            <semester_code> : One of the following codes, [S, F, W, U]
            -n              : Optional. If passed, will search the output of the previous search.
                                Otherwise, searches the whole course calendar.
        """
        search_array = self.all_courses
        sem = ''
        args = args.split(' ')

        if args[0] == '':
            print("[E] Please provide an argument")
            print(self.do_search_semester.__doc__)
            return

        # Check for -n, if there is carryover_data, search it instead of all_courses
        for arg in args:
            if arg == "-n":
                if self.carryover_data:
                    search_array = self.carryover_data

        # Find the first code
        for arg in args:
            if arg[0] != '-':
                sem = arg
                break

        if sem == 'F':
            sem = SemesterOffered.F
        elif sem == 'W':
            sem = SemesterOffered.W
        elif sem == 'S':
            sem = SemesterOffered.S
        elif sem == 'U':
            sem = SemesterOffered.U
        else:
            print("[E] Please enter a supported semester. [F, S, U, W]")
            return

        try:
            results = self.search.bySemester(search_array, sem)

            if results:
                self.carryover_data = results
                print("\n")
                for course in results:
                    print(course)
                print(f"Matched {len(results)}")
            else:
                print(f" No courses match semester '{sem}'")
        except ValueError as e:
            print(f"[E]: {e}")
        # }}}

    def do_search_weight(self, args):  # {{{
        """
        Search by credit weight.

        Usage: search_weight <weight> [-n]

            <weight> : The weight of the course. One of [0.0, 0.25, 0.5, 0.75, 1.0, 1.75, 2.0, 2.5,
                        2.75, 7.5]
            -n       : Optional. If passed, will search the output of the previous search.
                        Otherwise, searches the whole course calendar.
        """
        search_array = self.all_courses
        weight = ''
        float_weight = 0.0
        args = args.split(' ')

        if args[0] == '':
            print("[E] Please provide an argument")
            print(self.do_search_weight.__doc__)
            return

        # Check for -n, if there is carryover_data, search it instead of all_courses
        for arg in args:
            if arg == "-n":
                if self.carryover_data:
                    search_array = self.carryover_data

        # Find the first code
        for arg in args:
            if arg[0] != '-':
                weight = arg
                break

        try:
            float_weight = float(weight)
        except ValueError:
            print("\t[E] Not a floating point number. Or out of range")
            print(self.do_search_weight.__doc__)
            return

        try:
            results = self.search.byWeight(search_array, float_weight)

            if results:
                self.carryover_data = results
                print("\n")
                for course in results:
                    print(course)
                print(f"Matched {len(results)}")
            else:
                print(f" No courses match weight '{weight}'")
        except ValueError as e:
            print(f"[E]: {e}")
        # }}}


if __name__ == "__main__":
    Descriptr().cmdloop()
