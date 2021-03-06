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

        this.state = {
            courses: props.courses,
        };

        this.courseModal = React.createRef();

        // TODO: REMOVE DUMMY DATA ONCE SEARCH WORKING
        this.state.courses = [
            {
                group: 'Computing and Information Science',
                departments: ['School of Computer Science'],
                code: 'CIS',
                number: '1050',
                name: 'Web Design and Development',
                semesters_offered: ['S', 'W'],
                lecture_hours: 0.0,
                lab_hours: 0.0,
                credits: 0.5,
                description:
                    'An introduction to the basics of designing and developing a website. It examines the basic concepts, technologies, issues and techniques required to develop and maintain websites. The course is suitable for students with no previous programming experience.',
                distance_education: 'Offered through Distance Education format only.',
                prerequisites: [],
                equates: [],
                corequisites: [],
                restrictions: [],
                capacity_available: 3,
                capacity_max: 160,
                is_full: false,
            },
        ];
    }

    render() {
        return (
            <div>
                <CourseModal ref={this.courseModal} />
                <Table bordered hover responsive>
                    <thead className='thead-dark text-nowrap'>
                        <tr>
                            <th>Course</th>
                            <th>Name</th>
                            <th>Description</th>
                            <th>Credit Weight</th>
                        </tr>
                    </thead>
                    <tbody>
                        {this.state.courses.map((course) => (
                            <CourseTableRow
                                course={course}
                                showCourse={() => this.courseModal.current.showCourse(course)}
                                key={course.code + course.number.toString()}
                            />
                        ))}
                    </tbody>
                </Table>
            </div>
        );
    }
}
