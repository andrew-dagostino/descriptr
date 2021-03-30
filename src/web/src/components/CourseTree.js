import React from 'react';
import { TreeGraph } from './graph/treeGraph';
import { Card, Button, Row, Col } from 'react-bootstrap';
import CourseCodeSearch from './CourseCodeSearch';

export default class CourseTree extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            courses: {},
            downloadEnabled: false,
        };

        this.updateCourses = this.updateCourses.bind(this);
    }

    updateCourses = (courses) => this.setState({ courses: courses, downloadEnabled: courses && Object.keys(courses).length });

    render() {
        return (
            <div className="bg-light">
                <Card body className='my-5'>
                    <Card.Title>Course Search</Card.Title>
                    <CourseCodeSearch updateCourses={this.updateCourses} />
                </Card>
                <Card body>
                    <section className="Main">
                        <Row className='justify-content-between mb-4'>
                            <Col xs='auto' className='my-auto'>
                                <h5>Prerequisite Tree Graph</h5>
                            </Col>
                            <Col xs='auto'>
                                <Button id='download-tree-graph' variant='primary' disabled={!this.state.downloadEnabled}>
                                    Download Graph
                                </Button>
                            </Col>
                        </Row>
                        <TreeGraph coursesData={this.state.courses} />
                    </section>
                </Card>
            </div>
        )
    }
}