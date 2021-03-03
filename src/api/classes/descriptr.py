import json
import os
import sys
import re
import glob
import time
from enum import Enum

from classes.course_enums import SemesterOffered
from classes.course_parser import CourseParser
from classes.course_encoder import CourseEncoder
from classes.descriptr_searches import DescSearches
from classes.pdf_converter import PDFConverter
from functions.parse_scrape import add_course_capacity
from functions.save_webadvisor_courses import scrape_and_parse_webadvisor_courses


class Descriptr():
    """
    Stores and enables searches of courses within the WebAdvisor course calendar.

    Methods:
        apply_filters(filters):
            Searches using multiple filters in the provided filters dictionary, returning a JSON result
        export_json():
            Generates a JSON representation of carryover_data, with error message if applicable

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
        do_search_lec_hours(args):
            Search by number of lecture hours.
        do_search_lab_hours(args):
            Search by number of lab hours.
        do_search_capacity(args):
            Search by available capacity.
    """

    def __init__(self):
        """Use PDFConverter to convert Course Cal to text. Init cmd loop."""
        filepath = 'c12.pdf'
        if len(sys.argv) > 1:
            for i in range(1, len(sys.argv)):
                if(re.match(".+\\.pdf", sys.argv[i])):
                    filepath = sys.argv[i]
                    break

        self._load(filepath)

        latest_file = None

        if os.getenv("SCRAPE") != "OFF":
            for i in range(0, 2):  # i should only be 0 or 1 (single retry)
                try:
                    latest_file = max(glob.iglob(
                        "webadvisor-courses/*.html"), key=os.path.getctime)
                    if (time.time() - os.path.getctime(latest_file)) > 86400:
                        raise Exception
                    elif i == 0:
                        print(
                            "Retrieved cached WebAdvisor scrape made less than 24h ago. (" + latest_file + ")")
                    else:
                        print(
                            "Successfully scraped and saved WebAdvisor. (" + latest_file + ")")
                    break
                except (ValueError, Exception) as e:
                    if i == 0:  # Only scrape WebAdvisor once to avoid DoS
                        scrape_and_parse_webadvisor_courses()
                    else:
                        print(
                            "[W] Error while scraping WebAdvisor. Courses may not have updated capacity information.")

        self.all_courses = add_course_capacity(self.all_courses)

    def _load(self, filepath):
        """
            Initialize from PDF
        """
        converter = PDFConverter()
        parser = CourseParser()

        converter.openPDF(filepath)

        self.all_courses = parser.open_file("converted-pdf.txt")

        self.carryover_data = []  # A copy of data returned from search here.
        self.search = DescSearches()

    def apply_filters(self, filters):
        """
            Given an object of filters, performs all searches and returns the results as a JSON
            @param {String|Dict}    filters     A stringified JSON object or a dictionary of the filters to be applied
            @returns {String} A stringified JSON object of the courses after applying the filters, and an error if applicable
        """
        self.carryover_data = self.all_courses

        try:
            if type(filters) != dict:
                filters = json.loads(filters)

            for key, value in filters.items():
                if key == "code":
                    self.do_search_code(f"{value}", carryover=True)
                elif key == "group":
                    self.do_search_group(f"{value}", carryover=True)
                elif key == "department":
                    self.do_search_department(f"{value}", carryover=True)
                elif key == "keyword":
                    self.do_search_keyword(f"{value}", carryover=True)
                elif key == "level":
                    self.do_search_level(f"{value}", carryover=True)
                elif key == "number":
                    self.do_search_number(f"{value}", carryover=True)
                elif key == "semester":
                    self.do_search_semester(f"{value.upper()}", carryover=True)
                elif key == "weight":
                    self.do_search_weight(f"{value}", carryover=True)
                elif key == "capacity":
                    search_capacity = value.get("capacity")
                    search_comparison = value.get("comparison", "=")
                    self.do_search_capacity(
                        f"{search_capacity}", f"{search_comparison}", carryover=True)
                elif key == "lecture":
                    search_hours = value.get("hours")
                    search_comparison = value.get("comparison", "=")
                    self.do_search_lec_hours(
                        f"{search_hours}", f"{search_comparison}", carryover=True)
                elif key == "lab":
                    search_hours = value.get("hours")
                    search_comparison = value.get("comparison", "=")
                    self.do_search_lab_hours(
                        f"{search_hours}", f"{search_comparison}", carryover=True)
                elif key == "offered":
                    offered = ""
                    if value == True:
                        offered = "Y"
                    elif value == False:
                        offered = "N"
                    self.do_search_offered(f"{offered}", carryover=True)

        except Exception as e:
            self.carryover_data = []
            return json.dumps({
                "error": str(e),
                "courses": []
            })

        return self.export_json()

    def export_json(self):
        """
            Export a JSON representation of courses contained in the carryover_data
            @returns {String} JSON object containing an array of courses, and error if applicable
        """
        try:
            return json.dumps({
                "error": None,
                "courses": self.carryover_data
            }, cls=CourseEncoder)
        except Exception as e:
            return json.dumps({
                "error": str(e),
                "courses": []
            })

    def _perform_search(self, args, function, carryover=False, converter=None, join=True):
        search_array = self.carryover_data
        if not carryover:
            search_array = self.all_courses

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

        self.carryover_data = function(search_array, search_parameter)

    def do_search_code(self, *args, carryover=False):
        """
        Search by course code.
        @param {String}     args        The course letters e.g. CIS
        @param {Boolean}    carryover   True to search within previous results, False to search all courses
        """
        self._perform_search(
            args, self.search.byCourseCode, carryover=carryover)

    def do_search_group(self, *args, carryover=False):  # {{{
        """
        Search by course group.
        @param {String}     args        The course group e.g. Accounting
        @param {Boolean}    carryover   True to search within previous results, False to search all courses
        """
        self._perform_search(
            args, self.search.byCourseGroup, carryover=carryover)

    def do_search_department(self, *args, carryover=False):
        """
        Search by course department.
        @param {String}     args        The course department e.g. Department of Clinical Studies
        @param {Boolean}    carryover   True to search within previous results, False to search all courses
        """
        self._perform_search(
            args, self.search.byDepartment, carryover=carryover)

    def do_search_keyword(self, *args, carryover=False):
        """
        Search by keyword in the course.
        @param {String}     args        The term to search for eg. biology
        @param {Boolean}    carryover   True to search within previous results, False to search all courses
        """
        self._perform_search(args, self.search.byKeyword, carryover=carryover)

    def do_search_level(self, *args, carryover=False):
        """
        Search by level of a course.
        @param {String}     args        The leading number of a course code eg. 4 for a 4XXX course
        @param {Boolean}    carryover   True to search within previous results, False to search all courses
        """
        self._perform_search(
            args, self.search.byCourseLevel, carryover=carryover)

    def do_search_number(self, *args, carryover=False):
        """
        Search by full course number.
        @param {String}     args        The number of a course eg. 2750
        @param {Boolean}    carryover   True to search within previous results, False to search all courses
        """
        self._perform_search(
            args, self.search.byCourseNumber, carryover=carryover)

    def semester_converter(self, semester):
        try:
            return SemesterOffered[semester]
        except:
            print("[E] Please enter a supported semester. [F, S, U, W]")
        return

    def do_search_semester(self, *args, carryover=False):
        """
        Search by semester.
        @param {String}     args        One of the following codes, [S, F, W, U]
        @param {Boolean}    carryover   True to search within previous results, False to search all courses
        """
        self._perform_search(args, self.search.bySemester,
                             self.semester_converter, carryover=carryover)

    def weight_converter(self, weight):
        try:
            return float(weight)
        except:
            print("[E] Not a floating point number or out-of-range.")
        return

    def do_search_weight(self, *args, carryover=False):
        """
        Search by credit weight.
        @param {String}     args        The weight of the course. One of [0.0, 0.25, 0.5, 0.75, 1.0, 1.75, 2.0, 2.5, 2.75, 7.5]
        @param {Boolean}    carryover   True to search within previous results, False to search all courses
        """
        self._perform_search(args, self.search.byWeight,
                             self.weight_converter, carryover=carryover)

    def do_search_capacity(self, *args, carryover=False):
        """
        Search by available capacity.
        @param {String}     args        The available capacity of a course. Must be non-negative.
                                        How to perform the comparision. One of ["=", ">", "<"]. Defaults to "=".
        @param {Boolean}    carryover   True to search within previous results, False to search all courses
        """
        search_array = []
        if carryover:
            search_array = self.carryover_data
        else:
            search_array = self.all_courses

        comp = '='
        capacity = ''
        int_capacity = 0.0

        args = args.split(' ')
        if args[0] == '':
            print("[E] Please provide an argument")
            return

        # Find the first code
        for arg in args:
            if arg[0] not in ['-', '=', '>', '<']:
                capacity = arg
            elif arg[0] in ['=', '>', '<']:
                comp = arg

        try:
            int_capacity = int(capacity)
        except ValueError:
            print("\t[E] Not an integer or out of range.")
            return

        try:
            self.carryover_data = self.search.byCapacity(
                search_array, int_capacity, comp)
        except ValueError as e:
            print(f"[E]: {e}")

    def do_search_lec_hours(self, *args, carryover=False):
        """
        Search by lecture hours.
        @param {String}     args        The number of hours of lecture for the course. Must be non-negative
                                        How to perform the comparision. One of ["=", ">", "<"]. Defaults to "=".
        @param {Boolean}    carryover   True to search within previous results, False to search all courses
        """
        search_array = []
        if carryover:
            search_array = self.carryover_data
        else:
            search_array = self.all_courses

        comp = '='
        hours = ''
        float_hours = 0.0

        args = args.split(' ')
        if args[0] == '':
            print("[E] Please provide an argument")
            return

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
            return

        try:
            self.carryover_data = self.search.byLectureHours(
                search_array, float_hours, comp)
        except ValueError as e:
            print(f"[E]: {e}")

    def do_search_lab_hours(self, *args, carryover=False):
        """
        Search by lab hours.
        @param {String}     args        The number of hours of lab for the course. Must be non-negative
                                        How to perform the comparision. One of ["=", ">", "<"]. Defaults to "=".
        @param {Boolean}    carryover   True to search within previous results, False to search all courses
        """
        search_array = []
        if carryover:
            search_array = self.carryover_data
        else:
            search_array = self.all_courses

        comp = '='
        hours = ''
        float_hours = 0.0

        args = args.split(' ')
        if args[0] == '':
            print("[E] Please provide an argument")
            return

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
            return

        try:
            self.carryover_data = self.search.byLabHours(
                search_array, float_hours, comp)
        except ValueError as e:
            print(f"[E]: {e}")

    def offered_converter(self, offered):
        args = offered.split(" ")
        for arg in args:
            if arg.lower() == "y":
                return True
            if arg.lower() == "n":
                return False
        return

    def do_search_offered(self, *args, carryover=False):
        """
        Search by if a course is currently offered or not.
        @param {String}     args        Y/N. Only returns offered courses if Y and only returns unoffered courses if N.
        @param {Boolean}    carryover   True to search within previous results, False to search all courses
        """
        self._perform_search(args, self.search.byOffered,
                             self.offered_converter, carryover=carryover)
