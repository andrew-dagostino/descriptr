import React from 'react';
import CourseTable from './components/CourseTable';
import Search from './components/Search';

export default class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            courses: [],
        };

        this.updateCourses = this.updateCourses.bind(this);
    }

    updateCourses = (courses) => this.setState({ courses: courses });

    render() {
        return (
            <div className='App' style={{ padding: '100px' }}>
                <Search updateCourses={this.updateCourses} />
                <CourseTable courses={this.state.courses} />
            </div>
        );
    }
}
