/*
 * Search.js
 */

function Search() {
  /* Accepts a list of courses and displays some information of the Course JSON data in a table.

    Props:
      - courses (list<object>): The courses to display.
          Uses fields code, number, name, description, and credits.
  */

  return (
    <div style={{overflow: "hidden", width: "100%"}}>
      <div style={{float: "left"}}>
        Search filters
      </div>
      <br/>
      <div style={{overflow: "hidden", width: "100%"}}>
        <select name="fields" id="fields" style={{float: "left", width: "20%"}}>
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
        <select name="comparators" id="comparators" style={{float: "left", width: "20%"}}>
          <option value="contains">contains</option>
          <option value="isExact">is (exactly)</option>
          <option value="startsWith">starts with</option>
          <option value="greaterThan">greater than</option>
          <option value="lessThan">less than</option>
          <option value="greaterEqual">greater or equal to</option>
          <option value="lessEqual">less or equal to</option>
        </select>
        <input type="text" id="searchTerm" name="searchTerm" placeholder="Enter a search term" style={{width: "60%", height: "25px"}}></input>
      </div>
      <br/>
      <div id="addDiv" style={{overflow: "hidden", width: "100%"}}>
        <select name="logic" id="logic" style={{float: "left", width: "10%"}}>
          <option value="AND">AND</option>
          <option value="OR">OR</option>
          <option value="NOT">NOT</option>
        </select>
        <select name="fields" id="fields" style={{float: "left", width: "20%"}}>
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
        <select name="comparators" id="comparators" style={{float: "left", width: "20%"}}>
          <option value="contains">contains</option>
          <option value="isExact">is (exactly)</option>
          <option value="startsWith">starts with</option>
          <option value="greaterThan">greater than</option>
          <option value="lessThan">less than</option>
          <option value="greaterEqual">greater or equal to</option>
          <option value="lessEqual">less or equal to</option>
        </select>
        <input type="text" id="searchTerm" name="searchTerm" placeholder="Enter a search term" style={{width: "50%", height: "25px"}}></input>
      </div>
      <br/>
      <div style={{overflow: "hidden", width: "100%"}}>
        <button
          type="button"
          style={{float: "left", width: "150px", height: "50px"}}
          className="bg-secondary text-white"
        >Add Search Term</button>
        <button
          type="button"
          style={{float: "left", width: "150px", height: "50px"}}
          className="bg-danger text-white"
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

export default Search;
