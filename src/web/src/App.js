import React from 'react';
import CourseTable from './components/CourseTable';
import Search from './components/Search';
import { ForceGraph } from './components/graph/forceGraph'

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

    hoverTool(node) {
        
    }

    render() {
        return (
            <div className='App' style={{ padding: '100px' }}>
                <Search updateCourses={this.updateCourses} />
                <CourseTable courses={this.state.courses} />
                <section className="Main">
                    <ForceGraph linksData={data.links} nodesData={data.nodes} nodeHoverTooltip={this.nodeHoverTooltip} />
                </section>
            </div>
        );
    }
}
