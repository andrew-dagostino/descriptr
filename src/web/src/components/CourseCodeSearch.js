import React from 'react';
import { Form, Button, Row, Col } from 'react-bootstrap';

const isProd = /^file/.test(window.location) || /^https:\/\/cis4250-03\.socs\.uoguelph\.ca/.test(window.location); // Check if executable or prod web server

export default class CourseCodeSearch extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            code: "",
            number: 0,
        };

        this.onSubmit = this.onSubmit.bind(this);
    }

    onSubmit = () => {
        let courseID = this.state.code + '-' + String(this.state.number);
        fetch(isProd ?  'https://cis4250-03.socs.uoguelph.ca/api/prerequisite/' + courseID : 'api/prerequisite/' + courseID, {
            method: 'GET',
        })
            .then((response) => response.json())
            .then((data) => {
                if (!Array.isArray(data)) {
                    this.props.updateCourses(data)
                }
                else {
                    this.props.updateCourses({})
                }
            })
            .catch(err => console.log(err))
    }

    render() {
        return (
            <div>
                <Row className='my-3'>
                    <Col xs='auto'>
                        <Form.Control type='text' placeholder='Enter course code' value={this.state.code} onChange={e => this.setState({ code: e.target.value })} />
                    </Col>
                    <h3>*</h3>
                    <Col xs='auto'>
                        <Form.Control type='number' placeholder='Enter course number' value={this.state.number} onChange={e => this.setState({ number: e.target.value })} />
                    </Col>
                </Row>
                <p>   e.g. PSYC*1000</p>
                <Row bsPrefix='form-row' className='mt-3'>
                    <Col xs='auto'>
                        <Button
                            variant='danger'
                            type='button'
                        >
                            Clear Search
                        </Button>
                    </Col>
                    <Col xs='auto'>
                        <Button type='button' variant='primary' onClick={this.onSubmit} >
                            Search
                        </Button>
                    </Col>
                </Row>
            </div>   
        )
    }
}