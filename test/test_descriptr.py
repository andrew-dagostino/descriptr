import contextlib
import io
import os
import unittest

from app import Descriptr


class TestDescriptr(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.f = io.StringIO()
        with contextlib.redirect_stdout(self.f):  # Hide stdout from console during unit tests
            self.descriptr = Descriptr()

    def setUp(self):
        self.f = io.StringIO()  # Clear stored stdout for each test

    def test_load_pdf(self):
        """
            Test that the load_pdf command works
        """
        temp_courses = self.descriptr.all_courses
        self.descriptr.all_courses = []

        with contextlib.redirect_stdout(self.f):
            self.descriptr.onecmd("load_pdf test/test-pdf/mypdf.pdf")

        self.assertTrue(len(self.descriptr.all_courses) > 0)

        self.descriptr.all_courses = temp_courses  # restore original course list

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

        self.descriptr.all_courses = temp_courses  # restore original course list

    def test_export_graph(self):
        """Test that a graph can be exported under normal conditions."""
        with contextlib.redirect_stdout(self.f):
            self.descriptr.onecmd("export_graph testall")

        # Output to user is correct
        self.assertTrue("testall.csv" in self.f.getvalue())
        # Assert file is created
        self.assertTrue(os.path.exists("testall.csv"))
        # Assert that the file has the appropriate lines
        with open("testall.csv") as fopen:
            self.assertGreater(sum(1 for line in fopen), 1000)

        # File cleanup
        os.remove("testall.csv")

    def test_export_graph_filtered(self):
        """Test that a graph can be exported using the '-n' flag."""
        out_name = "test2750"
        out_file = f"{out_name}.csv"
        with contextlib.redirect_stdout(self.f):
            self.descriptr.onecmd("search_number 2750")
            self.descriptr.onecmd(f"export_graph {out_name} -n")

        # Output to user is correct
        self.assertTrue(out_file in self.f.getvalue())
        # Assert file is created
        self.assertTrue(os.path.exists(out_file))
        # Assert that the file has the appropriate lines
        with open(out_file) as fopen:
            self.assertEqual(sum(1 for line in fopen), 3)

        # File cleanup
        os.remove(out_file)

    def test_export_graph_invalid(self):
        """Test that export_graph refuses a bad filename."""
        out_name = "asdf876a98s7d6f0343#$%^&*()"
        with contextlib.redirect_stdout(self.f):
            self.descriptr.onecmd("search_number 2750")
            self.descriptr.onecmd(f"export_graph {out_name} -n")

        # Output to user is correct
        self.assertTrue("INVALID_CHARACTER" in self.f.getvalue())


if __name__ == '__main__':
    unittest.main()
