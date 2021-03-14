/**
 * CourseTable2.js
 *
 * Accepts a list of courses and displays some information of the Course JSON data in a table.
 *
 * Props:
 *  - courses (list<object>): The courses to display.
 */

import React from 'react';

import { useTable, usePagination } from 'react-table';
import { Row, Col, Form, Table, Pagination, InputGroup } from 'react-bootstrap';
import CourseModal from './CourseModal';

function CourseTable2(props) {
    const courseModal = React.createRef();

    const coursesIn = props.courses

    // Add a 'fullname' attribute to the course objects so we don't have to calculate it later.
    const data = React.useMemo(() =>
        coursesIn.map((course) => ({ ...course,
            fullname: `${course.code.toUpperCase()}*${course.number}`,
        })), [coursesIn])

    // Declare headers for the table and the corresponding fields to access in the data.
    const columns = React.useMemo(() => [
        {Header: 'Course', accessor: 'fullname'},
        {Header: 'Name', accessor: 'name'},
        {Header: 'Decription', accessor: 'description'},
        {Header: 'Credit Weight', accessor: 'credits'}
    ], [])

    // Initialize a bunch of functions and components from 'react-table' with our data and headers.
    const {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        prepareRow,
        page,
        canPreviousPage,
        canNextPage,
        pageCount,
        pageOptions,
        gotoPage,
        nextPage,
        previousPage,
        setPageSize,
        state: { pageIndex, pageSize },
    } = useTable(
        {
            columns,
            data,
            initialState: { pageIndex: 0 },
        }, usePagination
    )

    return (
        <div>
            <CourseModal ref={courseModal} />
            <Table {...getTableProps()} bordered hover responsive>
                <thead className='bg-secondary text-nowrap text-white'>
                    {/* Using react-table functions to render our header data into elements. */}
                    {headerGroups.map(headerGroup => (
                        <tr {...headerGroup.getHeaderGroupProps()}>
                            {headerGroup.headers.map(column => (
                                <th {...column.getHeaderProps()}>
                                    {column.render('Header')}
                                </th>
                            ))}
                        </tr>
                    ))}
                </thead>
                <tbody {...getTableBodyProps()}>
                    {/* react-table.pages contain rows and can be controlled with *Page methods. */}
                    {/* Render all the rows in 1 page. */}
                    {page.map((row, i) => {
                        prepareRow(row)
                        return (
                            <tr
                                {...row.getRowProps()}
                                onClick={() => courseModal.current.showCourse(row.original)}
                                style={{ cursor: 'pointer' }}>
                                {row.cells.map(cell => {
                                    return <td {...cell.getCellProps()}>
                                        {cell.render('Cell')}
                                    </td>
                                })}
                            </tr>
                        )
                    })}
                </tbody>
            </Table>
            {/* Pagination bar. The buttons call the functions to control the displayed page. */}
            <Row style={{alignItems: 'baseline'}}>
                <Col xs="auto">
                    <Pagination>
                        <Pagination.First onClick={() => gotoPage(0)} disabled={!canPreviousPage} />
                        <Pagination.Prev onClick={() => previousPage()} disabled={!canPreviousPage} />
                        <Pagination.Next onClick={() => nextPage()} disabled={!canNextPage} />
                        <Pagination.Last onClick={() => gotoPage(pageCount - 1)} disabled={!canNextPage} />
                    </Pagination>
                </Col>
                <Col xs="auto">
                    <span>
                        Page{' '}
                        <strong>
                            {pageIndex + 1} of {pageOptions.length}
                        </strong>
                    </span>
                </Col>
                {/* Direct page navigation by entering a number. */}
                <Col xs="auto">
                    <InputGroup>
                        <InputGroup.Prepend>
                            <InputGroup.Text>Go to page</InputGroup.Text>
                        </InputGroup.Prepend>
                    <Form.Control
                        type='number'
                        defaultValue={pageIndex + 1}
                        onChange={e => {
                            const page = e.target.value ? Number(e.target.value) - 1 : 0
                            gotoPage(page)
                        }}
                    />

                    </InputGroup>
                </Col>
                {/* Adjust the number of displayed rows in a page. */}
                <Col xs="auto">
                    <Form.Control
                        as='select'
                        value={pageSize}
                        onChange={e => {
                            setPageSize(Number(e.target.value))
                        }}
                    >
                        {[10, 20, 30, 40, 50].map(pageSize => (
                            <option key={pageSize} value={pageSize}>
                                Show {pageSize}
                            </option>
                        ))}
                    </Form.Control>
                </Col>
            </Row>
        </div>
    );
}
export default CourseTable2;
