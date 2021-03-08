/**
 * CourseTable.js
 *
 * Accepts a list of courses and displays some information of the Course JSON data in a table.
 *
 * Props:
 *  - courses (list<object>): The courses to display.
 */

import React from 'react';

import { Table } from 'react-bootstrap';
import CourseTableRow from './CourseTableRow';
import CourseModal from './CourseModal';

export default class CourseTable extends React.Component {
    constructor(props) {
        super(props);

        this.courseModal = React.createRef();
    }

    render() {
        return (
            <div>
                <CourseModal ref={this.courseModal} />
                <Table bordered hover responsive>
                    <thead className='bg-secondary text-nowrap text-white'>
                        <tr>
                            <th>Course</th>
                            <th>Name</th>
                            <th>Description</th>
                            <th>Credit Weight</th>
                        </tr>
                    </thead>
                    <tbody>
                        {this.props.courses.map((course) => (
                            <CourseTableRow
                                course={course}
                                showCourse={() => this.courseModal.current.showCourse(course)}
                                key={course.code + course.number}
                            />
                        ))}
                    </tbody>
                </Table>
            </div>
        );
    }
}
