/*
 * CourseTable.js
 */

function CourseTable({courses}) {
  /* Accepts a list of courses and displays some information of the Course JSON data in a table.

    Props:
      - courses (list<object>): The courses to display.
          Uses fields code, number, name, description, and credits.
  */
  const rows = courses.map((course) =>
    <tr key={course.code + course.number.toString()}>
      <th scope="row">{`${course.code.toUpperCase()}*${course.number}`}</th>
      <td>{course.name}</td>
      <td>{course.description}</td>
      <td>{course.credits}</td>
    </tr> 
  );
  return (
    <table className="table table-bordered table-hover">
      <thead>
        <tr>
          <th scope="col">Course</th>
          <th scope="col">Name</th>
          <th scope="col">Description</th>
          <th scope="col">Credit Weight</th>
        </tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>
  );
}

export default CourseTable;
