/**
 * Search.js
 */

import React from 'react';
import { Alert, Button, Col, Row } from 'react-bootstrap';
import SearchRow from '../components/SearchRow.js';

// Fields that will make use of >, <, and = comparisons
const numericalFields = ['lecture', 'lab', 'capacity'];
const isProd = /^file/.test(window.location) || /^https:\/\/cis4250-03\.socs\.uoguelph\.ca/.test(window.location); // Check if executable or prod web server

export default class Search extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            rows: [this.createEmptyFilter()],
            error: null,
        };
    }

    // Creates a new filter, with default values where necessary
    createEmptyFilter = () => ({
        searchType: 'code',
        searchComparator: '=',
        searchQuery: '',
    });

    // Appends a new, base filter
    addFilter = () => {
        this.setState({
            rows: this.state.rows.concat([this.createEmptyFilter()]),
        });
    };

    // Updates an individual filter by index
    updateFilter = (index, filter) => {
        let temp = this.state.rows;
        temp[index] = filter;
        this.setState({ rows: temp });
    };

    // Converts the array of filters from the state to a request body the API server can understand
    convertToRequestBody = () => {
        let request = {};
        let incomplete = 0;

        for (let filter of this.state.rows) {
            if (filter.searchType && filter.searchComparator && filter.searchQuery) {
                if (numericalFields.includes(filter.searchType)) {
                    if (filter.searchType === 'capacity') {
                        request[filter.searchType] = {
                            capacity: filter.searchQuery,
                            comparison: filter.searchComparator,
                        };
                    } else {
                        request[filter.searchType] = {
                            hours: filter.searchQuery,
                            comparison: filter.searchComparator,
                        };
                    }
                } else {
                    request[filter.searchType] = {
                        query: filter.searchQuery,
                        comparison: filter.searchComparator,
                    };
                }
            } else {
                incomplete++;
            }
        }

        if (incomplete > 0) {
            alert(`${incomplete} filter(s) were not fully filled out and were not sent`);
        }

        return request;
    };

    // Send filters as a POST to API server
    onSubmit = () => {
        fetch(isProd ? 'https://cis4250-03.socs.uoguelph.ca/api/search' : '/api/search', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(this.convertToRequestBody()),
        })
            .then((response) => response.json())
            .then((data) => {
                let courses = data.error ? [] : data.courses;
                this.props.updateCourses(courses.map((course) => JSON.parse(course)));
                this.setState({ error: data.error });
            });
    };

    render() {
        return (
            <>
                {this.state.error ? <Alert variant='danger'>{this.state.error}</Alert> : null}
                {this.state.rows.map((item, id) => {
                    return <SearchRow key={id} index={id} filter={item} updateFilter={this.updateFilter} />;
                })}
                <Row bsPrefix='form-row' className='mt-3'>
                    <Col xs='auto'>
                        <Button
                            variant='danger'
                            type='button'
                            onClick={() =>
                                this.setState({
                                    rows: [this.createEmptyFilter()],
                                })
                            }>
                            Clear Searches
                        </Button>
                    </Col>
                    <Col xs='auto'>
                        <Button variant='secondary' type='button' onClick={this.addFilter}>
                            Add Search Term
                        </Button>
                    </Col>
                    <Col xs='auto'>
                        <Button type='button' variant='primary' onClick={this.onSubmit}>
                            Search
                        </Button>
                    </Col>
                </Row>
            </>
        );
    }
}
