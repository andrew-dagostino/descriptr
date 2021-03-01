import logo from './logo.svg';
import './App.css';
import CourseTable from './components/CourseTable';

function App() {
    const mockCourses = [{
      code: "cis",
      number: 2750,
      name: "Software Systems Development and Integration",
      description: "This course introduces techniques and tools used in the development of large software systems. Students learn methods for organizing and constructing modular systems, manipulating files, introductory interface design, and use of databases. Software tools for managing projects, database connectivity, configuration management, and system application programmer interfaces are also covered.",
      credits: "0.5"},
      {'group': 'Computing and Information Science', 'departments': ['School of Computer Science'], 'code': 'CIS', 'number': '1050', 'name': 'Web Design and Development', 'semesters_offered': ['S', 'W'], 'lecture_hours': 0.0, 'lab_hours': 0.0, 'credits': 0.5, 'description': 'An introduction to the basics of designing and developing a website. It examines the basic concepts, technologies, issues and techniques required to develop and maintain websites. The course is suitable for students with no previous programming experience.', 'distance_education': 'Offered through Distance Education format only.', 'prerequisites': [], 'equates': [], 'corequisites': [], 'restrictions': [], 'capacity_available': 3, 'capacity_max': 160, 'is_full': false}
    ];
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Hello World!
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
      <CourseTable courses={mockCourses}/>
    </div>
  );
}

export default App;
