"""Contains a function to export a graphical representation of the courses."""

from jinja2 import Environment, FileSystemLoader
from pathvalidate import ValidationError, validate_filename


def export_graph(courses, path="out.csv"):  # {{{
    """
    Export a Course list as a CSV file to import into Gephi.

    Args:
        courses (list<Course>): The list of Courses to export.
        path (str): The output filepath. Default "out.csv".

    Raises:
        Exception: If unable to validate the passed path as valid. Or if unable
            to open the output file.

    Return:
        str: The name of the output file.
    """
    fout = "out.csv"

    # Validate filename
    try:
        validate_filename(path)
        if not path.endswith('.csv'):
            path = path + '.csv'
        fout = path
    except ValidationError as e:
        raise Exception(f"[E] Validation:Error {e}")

    # Template out the passed courses with Jinja2, see templates/out.csv.j2
    env = Environment(
            loader=FileSystemLoader("templates"),
            trim_blocks=True,
            lstrip_blocks=True
        )
    j2template = env.get_template('out.csv.j2')

    try:
        file_out = open(fout, "w")
    except Exception as e:
        raise(f"[E] Unable to open file {file_out}; {e}")
    with file_out:
        file_out.write(j2template.render(courses=courses))

    return fout
    # }}}
