/**
 * SearchRow.js
 */

import React from 'react';
import { Col, Form, Row } from 'react-bootstrap';

// Fields that will make use of >, <, and = comparisons
const numericalFields = ['lecture', 'lab', 'capacity'];

/**
 * SearchTypeDropdown
 *
 * Dropdown containing types of filters that can be used
 */
function SearchTypeDropdown(props) {
    const handleChange = (e) => props.setType(e.target.value);

    return (
        <Form.Control as='select' value={props.value} onChange={handleChange}>
            <option value='code'>Code</option>
            <option value='group'>Group</option>
            <option value='department'>Department</option>
            <option value='keyword'>Keyword</option>
            <option value='level'>Level</option>
            <option value='number'>Number</option>
            <option value='semester'>Semester</option>
            <option value='weight'>Weight</option>
            <option value='capacity'>Available Capacity</option>
            <option value='lecture'>Lecture Hours</option>
            <option value='lab'>Lab Hours</option>
            <option value='offered'>Currently Offered</option>
        </Form.Control>
    );
}

/**
 * SearchComparatorDropdown
 *
 * Dropdown containing ways to compare courses to the query
 *
 * Will change available options based on filter type passed through props
 */
function SearchComparatorDropdown(props) {
    const handleChange = (e) => props.setComparator(e.target.value);

    if (numericalFields.includes(props.type)) {
        return (
            <Form.Control as='select' value={props.value} onChange={handleChange}>
                <option value='>'>greater than</option>
                <option value='<'>less than</option>
                <option value='='>is (exactly)</option>
            </Form.Control>
        );
    } else if (props.type === 'weight' || props.type === 'offered' || props.type === 'semester') {
        return (
            <Form.Control as='select' value={props.value} onChange={handleChange}>
                <option value='='>is (exactly)</option>
            </Form.Control>
        );
    } else {
        return (
            <Form.Control as='select' value={props.value} onChange={handleChange}>
                <option value='~'>contains</option>
                <option value='='>is (exactly)</option>
            </Form.Control>
        );
    }
}

/**
 * SearchQueryInput
 *
 * Input for the query section of a filter.
 *
 * Will change between a text input, number input, or select based on filter type passed
 * through the props.
 */
function SearchQueryInput(props) {
    const handleChange = (e) => props.setQuery(e.target.value);

    if (numericalFields.includes(props.type)) {
        return <Form.Control type='number' value={props.value} placeholder='Enter a search term' onChange={handleChange} min={0} />;
    } else if (props.type === 'weight') {
        return (
            <Form.Control as='select' value={props.value} onChange={handleChange}>
                <option value='' disabled>
                    Choose an Option...
                </option>
                <option value='0.0'>0.0</option>
                <option value='0.25'>0.25</option>
                <option value='0.50'>0.50</option>
                <option value='0.75'>0.75</option>
                <option value='1.00'>1.00</option>
                <option value='1.75'>1.75</option>
                <option value='2.00'>2.00</option>
                <option value='2.50'>2.50</option>
                <option value='2.75'>2.75</option>
                <option value='7.50'>7.50</option>
            </Form.Control>
        );
    } else if (props.type === 'offered') {
        return (
            <Form.Control as='select' value={props.value} onChange={handleChange}>
                <option value='' disabled>
                    Choose an Option...
                </option>
                <option value='Y' selected>
                    Yes
                </option>
                <option value='N'>No</option>
            </Form.Control>
        );
    } else if (props.type === 'semester') {
        return (
            <Form.Control as='select' value={props.value} onChange={handleChange}>
                <option value='' disabled>
                    Choose an Option...
                </option>
                <option value='W'>Winter</option>
                <option value='F'>Fall</option>
                <option value='S'>Summer</option>
            </Form.Control>
        );
    } else {
        return <Form.Control type='text' value={props.value} placeholder='Enter a search term' onChange={handleChange} />;
    }
}

/**
 * SearchRow
 *
 * Represents a single filter in the search. Manages the state of its
 * three child components and updates itself in the parent's state
 */
export default class SearchRow extends React.Component {
    constructor(props) {
        super(props);

        // Temporary state, real state is managed in parent
        this.state = { ...this.props.filter };
    }

    // Update individual values in child state, then update full filter in parent state
    setType = (type) => this.setState({ searchType: type, searchComparator: '=', searchQuery: '' }, this.updateParent); // Reset on type change
    setComparator = (comparator) => this.setState({ searchComparator: comparator }, this.updateParent);
    setQuery = (query) => this.setState({ searchQuery: query }, this.updateParent);

    // Update full filter in parent state
    updateParent = () => this.props.updateFilter(this.props.index, this.state);

    render() {
        return (
            <Row className='my-3'>
                <Col xs='auto'>
                    <SearchTypeDropdown value={this.props.filter.searchType} setType={this.setType} />
                </Col>
                <Col xs='auto'>
                    <SearchComparatorDropdown
                        value={this.props.filter.searchComparator}
                        setComparator={this.setComparator}
                        type={this.state.searchType}
                    />
                </Col>
                <Col xs='auto'>
                    <SearchQueryInput value={this.props.filter.searchQuery} setQuery={this.setQuery} type={this.state.searchType} />
                </Col>
            </Row>
        );
    }
}
