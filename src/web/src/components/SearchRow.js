import React from 'react';

export default class SearchRow extends React.Component {
	render() {
		return (
			<div style={{overflow: "hidden", width: "100%", marginTop: "5px"}}>
				<select style={{float: "left", width: "10%", marginRight: "10px"}}>
					<option value="AND">AND</option>
					<option value="OR">OR</option>
					<option value="NOT">NOT</option>
				</select>
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
				<input type="text" placeholder="Enter a search term" style={{width: "calc(50% - 30px)", height: "25px"}}></input>
			</div>
		);
	}
}