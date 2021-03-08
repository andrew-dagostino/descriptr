import React from 'react';
import CourseTable from './components/CourseTable';
import TempSearch from './components/tempSearch'
import Search from './components/Search';
import { ForceGraph } from './components/graph/forceGraph';
import Header from './components/Header';
import { Card } from 'react-bootstrap';

const data = require('./components/graph/miserables.json');

export default class App extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      courses: [],
    };

    this.updateCourses = this.updateCourses.bind(this);
  }

  updateCourses = (courses) => this.setState({ courses: courses });
  nodeHoverTooltip = (node) => {
    return `<div>
            <b>${node.id}</b>
        </div>`;
  }

  render() {
    return (
      <div className="App bg-light">
        <Header />
        <section className="px-5 pb-5">
          <Card body className="my-5">
            <Card.Title>JSON search</Card.Title>
            <TempSearch courses={this.state.courses} updateCourses={this.updateCourses} />
          </Card>
          <Card body className="my-5">
            <Card.Title>Course Search</Card.Title>
            <Search updateCourses={this.updateCourses} />
          </Card>
          <Card body className="my-5">
            <Card.Title>Results</Card.Title>
            <CourseTable courses={this.state.courses} />
          </Card>
          <Card body>
            <section className="Main">
              <ForceGraph linksData={data.links} nodesData={data.nodes} nodeHoverTooltip={this.nodeHoverTooltip} />
            </section>
          </Card>
        </section>
      </div>
    );
  }
}
