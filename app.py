#!/usr/bin/env python3

import os
import sys
import re
from enum import Enum

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
from functions.export import export_graph
from functions.parse_scrape import add_course_capacity


class Descriptr(cmd.Cmd):
    """
    Represents a Read-Eval-Print Loop that interacts with the course calendar.

    Methods:
        do_exit():
            Exit Descriptr.
        do_export_graph():
            Export a CSV representation courses. Importable by Gephi.
        do_load_pdf():
            Parse and load a new courses PDF.
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

        #Run the scraping of web advisor
        if os.getenv("SCRAPE") != "OFF":
            import scripts.webadvisor.save_webadvisor_courses

        print("Getting capacity info from WebAdvisor data...")
        self.all_courses = add_course_capacity(self.all_courses)

        print("Loading Complete")

        super().__init__()  # Call to cmd Object's init
        # }}}

    def _load(self, filepath):
        converter = PDFConverter()
        parser = CourseParser()

        print("Converting...")
        converter.openPDF(filepath)

        print("Parsing...")
        self.all_courses = parser.open_file("converted-pdf.txt")

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

    def do_export_graph(self, args):
        """
        Export a CSV representation courses. Importable by Gephi.

        Usage: export_graph [<filename>] [-n]

            <filename> : Optional. The name of the exported CSV file. Default 'out.csv".
            -n         : Optional. If passed, will export a graph of the courses in the previous
                            search. Otherwise, outputs a graph of the whole course calendar.
        """
        search_array = self.all_courses
        filename = 'out.csv'
        args = args.split(' ')

        if args[0] != '':
            # Check for -n, if there is carryover_data, search it instead of all_courses
            for arg in args:
                if arg == "-n":
                    if self.carryover_data:
                        search_array = self.carryover_data

            # Find the first filepath
            for arg in args:
                if arg[0] != '-':
                    filename = arg
                    break

        try:
            file_created = export_graph(search_array, filename)
        except Exception as e:
            print(e)
            return None

        print(f"Graph exported at '{file_created}'")

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

    def perform_search(self, args, function, doc, converter = None, join = True):  # {{{

        args = args.split(' ')

        # Ensure arguments are provided
        if args[0] == '':
            print("[E] Please provide an argument")
            print(doc)
            return

        search_array = self.all_courses

        # Check for -n, if there is carryover_data, search it instead of all_courses
        for arg in args:
            if arg == "-n":
                if self.carryover_data:
                    search_array = self.carryover_data
                args.pop(args.index(arg))
                break

        # Join remaining arguments, and convert them if needed
        search_parameter = None
        if join:
            joined_args = " ".join(args)
            if converter != None:
                search_parameter = converter(joined_args)
            else:
                search_parameter = joined_args
        else:
            if converter != None:
                search_parameter = converter(args)
            else:
                search_parameter = args

        # Filter search array to the search parameter
        try:
            results = function(search_array, search_parameter)

            if results:
                self.carryover_data = results
                print("\n")
                for course in results:
                    print(course)
                print(f"Matched {len(results)}")
            else:
                print(f" No courses match search term '{ search_parameter }'")
        except ValueError as e:
            print(f"[E]: {e}")

    # }}}

    def do_search_code(self, args):  # {{{
        """
        Search by course code.

        Usage: search_code <course_code> [-n]

            <course_code> : The course letters e.g. CIS
            -n            : Optional. If passed, will search the output of the previous search.
                            Otherwise, searches the whole course calendar.
        """

        self.perform_search(args, self.search.byCourseCode, self.__doc__)

    # }}}

    def do_search_group(self, args):  # {{{
        """
        Search by course group.

        Usage: search_group <course_group> [-n]

            <course_group> : The course group e.g. Accounting
            -n             : Optional. If passed, will search the output of the previous search.
                            Otherwise, searches the whole course calendar.
        """

        self.perform_search(args, self.search.byCourseGroup, self.__doc__)

    # }}}

    def do_search_department(self, args):  # {{{
        """
        Search by department.

        Usage: search_department <department> [-n]

            <department> : The department e.g. Department of Clinical Studies
            -n           : Optional. If passed, will search the output of the previous search.
                            Otherwise, searches the whole course calendar.
        """

        self.perform_search(args, self.search.byDepartment, self.__doc__)

    # }}}

    def do_search_keyword(self, args):  # {{{
        """
        Search by keyword.

        Usage: search_keyword <keyword> [-n]

            <keyword> : The term to search e.g. biology
            -n        : Optional. If passed, will search the output of the previous search.
                        Otherwise, searches the whole course calendar.
        """

        self.perform_search(args, self.search.byKeyword, self.__doc__)

    # }}}

    def do_search_level(self, args):  # {{{
        """
        Search by course level.

        Usage: search_level <course_level> [-n]

            <course_level> : The leading number of a course number e.g. 3
            -n            : Optional. If passed, will search the output of the previous search.
                            Otherwise, searches the whole course calendar.
        """

        self.perform_search(args, self.search.byCourseLevel, self.__doc__)

    # }}}

    def do_search_number(self, args):  # {{{
        """
        Search by full course number, not just course level.

        Usage: search_number <course_number> [-n]

            <course_number> : The full number of a course e.g. 2750
            -n              : Optional. If passed, will search the output of the previous search.
                                Otherwise, searches the whole course calendar.
        """

        self.perform_search(args, self.search.byCourseNumber, self.__doc__)

    # }}}

    def semester_converter(self, semester):
        try:
            return SemesterOffered[semester]
        except:
            print("[E] Please enter a supported semester. [F, S, U, W]")
        return


    def do_search_semester(self, args):  # {{{
        """
        Search by semester.

        Usage: search_semester <semester_code> [-n]

            <semester_code> : One of the following codes, [S, F, W, U]
            -n              : Optional. If passed, will search the output of the previous search.
                                Otherwise, searches the whole course calendar.
        """

        self.perform_search(args, self.search.bySemester, self.__doc__, self.semester_converter)

    # }}}

    def weight_converter(self, weight):
        try:
            return float(weight)
        except:
            print("[E] Not a floating point number or out-of-range.")
        return

    def do_search_weight(self, args):  # {{{
        """
        Search by credit weight.

        Usage: search_weight <weight> [-n]

            <weight> : The weight of the course. One of [0.0, 0.25, 0.5, 0.75, 1.0, 1.75, 2.0, 2.5,
                        2.75, 7.5]
            -n       : Optional. If passed, will search the output of the previous search.
                        Otherwise, searches the whole course calendar.
        """

        self.perform_search(args, self.search.byWeight, self.__doc__, self.weight_converter)

    # }}}

    def do_search_lec_hours(self, args):  # {{{
        """
        Search by lecture hours.

        Usage: search_lec_hours <hours> [comparison] [-n]

            <hours>    : The number of hours of lecture for the course. Must be non-negative
            comparison : Optional. How to perform the comparison. One of ["=", ">", "<"]
            -n         : Optional. If passed, will search the output of the previous search.
                         Otherwise, searches the whole course calendar.
        """
        search_array = self.all_courses
        comp = '='
        hours = ''
        float_hours = 0.0
        args = args.split(' ')

        if args[0] == '':
            print("[E] Please provide an argument")
            print(self.do_search_lec_hours.__doc__)
            return

        # Check for -n, if there is carryover_data, search it instead of all_courses
        for arg in args:
            if arg == "-n":
                if self.carryover_data:
                    search_array = self.carryover_data

        # Find the first code
        for arg in args:
            if arg[0] not in ['-', '=', '>', '<']:
                hours = arg
            elif arg[0] in ['=', '>', '<']:
                comp = arg

        try:
            float_hours = float(hours)
        except ValueError:
            print("\t[E] Not a floating point number. Or out of range")
            print(self.do_search_lec_hours.__doc__)
            return

        try:
            results = self.search.byLectureHours(search_array, float_hours, comp)

            if results:
                self.carryover_data = results
                print("\n")
                for course in results:
                    print(course)
                print(f"Matched {len(results)}")
            else:
                print(f"No courses match lecture hours '{comp}{hours}'")
        except ValueError as e:
            print(f"[E]: {e}")
        # }}}

    def do_search_lab_hours(self, args):  # {{{
        """
        Search by lab hours.

        Usage: search_lab_hours <hours> [comparison] [-n]

            <hours>    : The number of hours of lab for the course. Must be non-negative
            comparison : Optional. How to perform the comparison. One of ["=", ">", "<"]
            -n         : Optional. If passed, will search the output of the previous search.
                         Otherwise, searches the whole course calendar.
        """
        search_array = self.all_courses
        comp = '='
        hours = ''
        float_hours = 0.0
        args = args.split(' ')

        if args[0] == '':
            print("[E] Please provide an argument")
            print(self.do_search_lec_hours.__doc__)
            return

        # Check for -n, if there is carryover_data, search it instead of all_courses
        for arg in args:
            if arg == "-n":
                if self.carryover_data:
                    search_array = self.carryover_data

        # Find the first code
        for arg in args:
            if arg[0] not in ['-', '=', '>', '<']:
                hours = arg
            elif arg[0] in ['=', '>', '<']:
                comp = arg

        try:
            float_hours = float(hours)
        except ValueError:
            print("\t[E] Not a floating point number. Or out of range")
            print(self.do_search_lec_hours.__doc__)
            return

        try:
            results = self.search.byLabHours(search_array, float_hours, comp)

            if results:
                self.carryover_data = results
                print("\n")
                for course in results:
                    print(course)
                print(f"Matched {len(results)}")
            else:
                print(f"No courses match lab hours '{comp}{hours}'")
        except ValueError as e:
            print(f"[E]: {e}")
        # }}}

    def offered_converter(self, offered):
        args = offered.split(" ")
        for arg in args:
            if arg.lower() == "y":
                return True
            if arg.lower() == "n":
                return False
        return

    def do_search_offered(self, args):
        """
        Search by if a course is currently offered or not.

        Usage: search_offered <offered> [-n]

            <offered> : Y/N. Only returns offered courses if Y and only returns unoffered courses if N.
            -n        : Optional. If passed, will search the output of the previous search.
                        Otherwise, searches the whole course calendar.
        """

        self.perform_search(args, self.search.byOffered, self.__doc__, self.offered_converter)

if __name__ == "__main__":
    Descriptr().cmdloop()
