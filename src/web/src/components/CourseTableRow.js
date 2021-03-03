/**
 * CourseTableRow.js
 *
 * Accepts a single course and displays its information as a table row.
 *
 * Props:
 *  - course (object): The course to display.
 */

export default function CourseTableRow(props) {
    let course = props.course;
    return (
        <tr>
            <td>{`${course.code.toUpperCase()}*${course.number}`}</td>
            <td>{course.name}</td>
            <td>{course.description}</td>
            <td>{course.credits}</td>
        </tr>
    );
}
