import React from "react"

import { Form, Button } from 'react-bootstrap'

let data = [
  {
      "group": "Computing and Information Science",
      "departments": ["School of Computer Science"],
      "code": "CIS",
      "number": "1050",
      "name": "Web Design and Development",
      "semesters_offered": ["S", "W"],
      "lecture_hours": 0.0,
      "lab_hours": 0.0,
      "credits": 0.5,
      "description":
          "An introduction to the basics of designing and developing a website. It examines the basic concepts, technologies, issues and techniques required to develop and maintain websites. The course is suitable for students with no previous programming experience.",
      "distance_education": "Offered through Distance Education format only.",
      "prerequisites": [],
      "equates": [],
      "corequisites": [],
      "restrictions": [],
      "capacity_available": 3,
      "capacity_max": 160,
      "is_full": false,
  },
];

export default class tempSearch extends React.Component {
  state = {
    value: "",
  };

  constructor(props) {
    super(props);
    this.onSubmit = this.onSubmit.bind(this);
  }

  onSubmit() {
    fetch('/api/search', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.state.value) })
      .then(response => response.json())
      .then(data=>{ 
        var str = JSON.stringify(data.courses);
        alert(str);
        this.props.updateCourses(data.courses.map((course) => JSON.parse(course))); 
      })
  }

  render() {
    return (
      <div>
        <Form>
          <Form.Group>
            <Form.Control 
              id="jsonText" 
              as="textarea" 
              rows={3} 
              value={this.state.value} 
              onChange={e => this.setState({ value: e.target.value })}
              type="text"
            />
          </Form.Group>
        </Form>
        <Button 
          variant="primary" 
          onClick={this.onSubmit}
        >
          Search
        </Button>
        <Button 
          variant="primary" 
          onClick={() => this.props.updateCourses(data)}
        >
          Test
        </Button>
      </div>
    );
  }
}