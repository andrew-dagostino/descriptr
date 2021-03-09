/*
 * Search.js
 */

import React from 'react';
import SearchRow from '../components/SearchRow.js';

export default class Search extends React.Component {
  /* Accepts a list of courses and displays some information of the Course JSON data in a table.

    Props:
      - courses (list<object>): The courses to display.
          Uses fields code, number, name, description, and credits.
  */

  constructor(props) {
    super(props);
    this.state = ({rows: []})
  }

  render() {
    return(
      <div style={{overflow: "hidden", width: "100%"}}>
        <div style={{float: "left"}}>
          Search filters
        </div>
        <br/>
        <div style={{overflow: "hidden", width: "100%"}}>
          <select style={{float: "left", width: "20%", marginRight: "10px"}}>
            <option value="group">Group</option>
            <option value="department">Department</option>
            <option value="code">Code</option>
            <option value="number">Number</option>
            <option value="name">Name</option>
            <option value="semester">Semester</option>
            <option value="lectureHours">Lecture Hours</option>
            <option value="labHours">Lab Hours</option>
            <option value="credits">Credits</option>
            <option value="description">Description</option>
            <option value="distanceEducation">Distance Education</option>
            <option value="yearParityRestriction">Year Parity Restriction</option>
            <option value="other">Other</option>
            <option value="prerequisite">Prerequisite</option>
            <option value="equate">Equate</option>
            <option value="corequisite">Corequisite</option>
            <option value="restrictions">Restrictions</option>
            <option value="capacityAvailable">Capacity Available</option>
            <option value="capacityMax">Capacity Max</option>
          </select>
          <select style={{float: "left", width: "20%", marginRight: "10px"}}>
            <option value="contains">contains</option>
            <option value="isExact">is (exactly)</option>
            <option value="startsWith">starts with</option>
            <option value="greaterThan">greater than</option>
            <option value="lessThan">less than</option>
            <option value="greaterEqual">greater or equal to</option>
            <option value="lessEqual">less or equal to</option>
          </select>
          <input type="text" placeholder="Enter a search term" style={{width: "calc(60% - 20px)", height: "25px"}}></input>
        </div>
        <br/>
        <div id="addDivParent" style={{overflow: "hidden", width: "100%"}}>
          {this.state.rows.map((item, id) => {
            return(
              <SearchRow/>
            );
          })}
        </div>
        <br/>
        <div style={{overflow: "hidden", width: "100%"}}>
          <button
            type="button"
            style={{float: "left", width: "150px", height: "50px", marginRight: "10px"}}
            className="bg-secondary text-white"
            onClick={() => {
              this.setState({rows: this.state.rows.concat([{}])});
            }}
          >Add Search Term</button>
          <button
            type="button"
            style={{float: "left", width: "150px", height: "50px"}}
            className="bg-danger text-white"
            onClick={() => {
              this.setState({rows: []});
            }}
          >Reset Search</button>
          <button
            type="button"
            style={{float: "right", width: "150px", height: "50px"}}
            className="bg-info text-white"
          >Search</button>
        </div>
      </div>
    );
  }
}