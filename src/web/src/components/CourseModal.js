/**
 * CourseModal.js
 *
 * Displays all information about a course as a modal.
 *
 * Props:
 *  - course (object): The course to display.
 */

import React from 'react';

import { Modal, Row, Col } from 'react-bootstrap';

export default class CourseModal extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            course: null,
            show: false,
        };
    }

    // Sets the course and shows the modal
    showCourse = (course) => {
        for (let key of Object.keys(course)) {
            course[key] = this._undefinedToNA(course[key]);
        }

        this.setState({
            course: course,
            show: true,
        });
    };

    // Hides the modal
    hide = () => this.setState({ show: false });

    // Changes null/undefined fields to "N/A"
    _undefinedToNA = (val) => (val != null ? val : 'N/A');

    render() {
        let course = this.state.course;
        if (course) {
            let prerequisites = [];
            if (course.prerequisites && course.prerequisites.simple?.length) {
                prerequisites = prerequisites.concat(course.prerequisites.simple);
            }
            if (course.prerequisites && course.prerequisites.complex?.length) {
                prerequisites = prerequisites.concat(course.prerequisites.complex);
            }

            return (
                <Modal show={this.state.show} onHide={this.hide} size='lg' centered>
                    <Modal.Header className='bg-warning text-black' closeButton>
                        <Modal.Title>
                            <h1 className='h3'>
                                {`${course.code.toUpperCase()}*${course.number} - ${course.name} ${course.semesters_offered.join(',')} [${parseFloat(
                                    course.credits,
                                ).toFixed(2)}]`}
                            </h1>
                            <h2 className='h4'>{course.departments.join(', ')}</h2>
                        </Modal.Title>
                    </Modal.Header>

                    <Modal.Body className='my-2'>
                        <Row>
                            <Col xs={3}>
                                <b>Available Capacity</b>
                            </Col>
                            <Col className={course.is_full ? 'text-danger' : ''}>{`${course.capacity_available} / ${course.capacity_max}`}</Col>
                            <Col xs={12}>
                                <i>Note: WebAdvisor capacity is only updated once per day and may be inaccurate</i>
                            </Col>
                        </Row>

                        <hr />

                        <Row>
                            <Col xs={3}>
                                <b>Description</b>
                            </Col>
                            <Col>{course.description}</Col>
                        </Row>
                        <br />
                        <Row>
                            <Col xs={3}>
                                <b>Distance Education</b>
                            </Col>
                            <Col>{course.distance_education}</Col>
                        </Row>
                        <Row>
                            <Col xs={3}>
                                <b>Lecture Hours</b>
                            </Col>
                            <Col>{course.lecture_hours}</Col>
                            <Col xs={3}>
                                <b>Lab Hours</b>
                            </Col>
                            <Col>{course.lab_hours}</Col>
                        </Row>
                        <br />
                        <Row>
                            <Col xs={3}>
                                <b>Prerequisites</b>
                            </Col>
                            <Col>{prerequisites.length ? prerequisites.map((prereq) => <div>{prereq}</div>) : 'None'}</Col>
                            <Col xs={3}>
                                <b>Corequisites</b>
                            </Col>
                            <Col>{course.corequisites.length ? <div>{course.corequisites}</div> : 'None'}</Col>
                        </Row>
                        <Row>
                            <Col xs={3}>
                                <b>Restrictions</b>
                            </Col>
                            <Col>{course.restrictions.length ? course.restrictions.map((restrict) => <div>{restrict}</div>) : 'None'}</Col>
                            <Col xs={3}>
                                <b>Equates</b>
                            </Col>
                            <Col>{course.equates.length ? <div>{course.equates}</div> : 'None'}</Col>
                        </Row>
                    </Modal.Body>
                </Modal>
            );
        } else {
            return null;
        }
    }
}
