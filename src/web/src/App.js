import React from 'react';
import { Card } from 'react-bootstrap';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

import CourseTable2 from './components/CourseTable2';
import Search from './components/Search';
import { ForceGraph } from './components/graph/forceGraph';
import Header from './components/Header';
import Help from './components/Help';

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
            <b>${node.name}</b>
        </div>`;
    };

    render() {
        return (
            <Router>
                <div className='App bg-light'>
                    <Header />
                    <Switch>
                        <Route path="/help">
                            <section className='px-5 pb-5'>
                                <Help />
                            </section>
                        </Route>
                        <Route path="/">
                            <section className='px-5 pb-5'>
                                <Card body className='my-5'>
                                    <Card.Title>Course Search</Card.Title>
                                    <Search updateCourses={this.updateCourses} />
                                </Card>
                                <Card body className='my-5'>
                                    <Card.Title>Results</Card.Title>
                                    <CourseTable2 courses={this.state.courses} />
                                </Card>
                                <Card body>
                                    <section className='Main'>
                                        <ForceGraph coursesData={this.state.courses} nodeHoverTooltip={this.nodeHoverTooltip} />
                                    </section>
                                </Card>
                            </section>
                        </Route>
                    </Switch>
                </div>
            </Router>
        );
    }
}
