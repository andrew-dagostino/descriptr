import contextlib
import io
import os
import unittest

from app import Descriptr

class TestDescriptr(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.f = io.StringIO()
        with contextlib.redirect_stdout(self.f): # Hide stdout from console during unit tests
            self.descriptr = Descriptr()

    def setUp(self):
        self.f = io.StringIO() # Clear stored stdout for each test

    def test_load_pdf(self):
        """
            Test that the load_pdf command works
        """
        temp_courses = self.descriptr.all_courses
        self.descriptr.all_courses = []

        with contextlib.redirect_stdout(self.f):
            self.descriptr.onecmd("load_pdf test/test-pdf/mypdf.pdf")

        self.assertTrue(len(self.descriptr.all_courses) > 0)

        self.descriptr.all_courses = temp_courses # restore original course list

    def test_load_pdf_invalid(self):
        """
            Test that the load_pdf command displays error to user if no pdf found
        """
        temp_courses = self.descriptr.all_courses
        self.descriptr.all_courses = []

        with contextlib.redirect_stdout(self.f):
            self.descriptr.onecmd("load_pdf dne")

        self.assertTrue(len(self.descriptr.all_courses) == 0)
        self.assertTrue("[E] Provided file must be a PDF" in self.f.getvalue())

        self.descriptr.all_courses = temp_courses # restore original course list

if __name__ == '__main__':
    unittest.main()