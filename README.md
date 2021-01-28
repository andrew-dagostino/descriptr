# UoG Course Descriptr.ly

[[_TOC_]]

## Requirements

- [Python 3](https://www.python.org/download/releases/3.0/)
- `pdftotext` v0.62.0

## Installation

1. Install `pdftotext` by installing `poppler-utils` with the following command:

    ```
    apt install poppler-utils
    ```

## Testing

Unit tests can be run with the following command while in the root directory:

```
python3 -m unittest
```

## Running

Use `python3 app.py` or `./app.py` to run Descriptr.

Descriptr has built in help. To list available commands type `?` or `help`. To get help for
a specific command, type `help <command>`. Or, see below.

## Help

Available commands:

| Command             | Short Description                                     |
| ---                 | ---                                                   |
| `exit`              | Exit Descriptr.                                       |
| `help`, `?`         | Print the list of commands and specific command help. |
| `search_code`       | Search by course code letters.                        |
| `search_department` | Search by department.                                 |
| `search_keyword`    | Search by keyword.                                    |
| `search_level`      | Search by course level.                               |
| `search_number`     | Search by course number.                              |
| `search_semester`   | Search by semester.                                   |
| `search_weight`     | Search by credit weight.                              |

### `exit`

```
Exit Descriptr.

    Usage:
        exit
```

### `help`, `?`

```
Print the list of commands and specific command help.

Usage:  help [<command>]
        ?

    <command> : The name of a command.
```

### `search_code`

```
Search by course code.

Usage: search_code <course_code> [-n]

    <course_code> : The course letters e.g. CIS
    -n            : Optional. If passed, will search the output of the previous search.
                    Otherwise, searches the whole course calendar.
```

### `search_department`

```
Search by department.

Usage: search_department <department> [-n]

    <department> : The department e.g. Department of Clinical Studies
    -n           : Optional. If passed, will search the output of the previous search.
                    Otherwise, searches the whole course calendar.
```

### `search_keyword`

```
Search by keyword.

Usage: search_keyword <keyword> [-n]

    <keyword> : The term to search e.g. biology
    -n        : Optional. If passed, will search the output of the previous search.
                Otherwise, searches the whole course calendar.
```

### `search_level`

```
Search by course level.

Usage: search_level <course_level> [-n]

    <course_level> : The leading number of a course number e.g. 3
    -n            : Optional. If passed, will search the output of the previous search.
                    Otherwise, searches the whole course calendar.
```

### `search_number`

```
Search by full course number, not just course level.

Usage: search_number <course_number> [-n]

    <course_number> : The full number of a course e.g. 2750
    -n              : Optional. If passed, will search the output of the previous search.
                        Otherwise, searches the whole course calendar.
```

### `search_semester`

```
Search by semester.

Usage: search_semester <semester_code> [-n]

    <semester_code> : One of the following codes, [S, F, W, U]
    -n              : Optional. If passed, will search the output of the previous search.
                        Otherwise, searches the whole course calendar.
```

### `search_weight`

```
Search by credit weight.

Usage: search_weight <weight> [-n]

    <weight> : The weight of the course. One of [0.0, 0.25, 0.5, 0.75, 1.0, 1.75, 2.0, 2.5,
                2.75, 7.5]
    -n       : Optional. If passed, will search the output of the previous search.
                Otherwise, searches the whole course calendar.
```


## Course Data Structure

### Course

* **Group:** 
    * `string`
    * e.g.
        * `Computing and Information Science`
        * `Accounting`
* **Departments:** 
    * `List<string>`
    * e.g.
        * `{ School of Computer Science }`
        * `{ Department of Management }`
        * `{ Dean's Office, College of Arts }`
* **Code:** 
    * `string`
    * e.g.
        * `CIS`
        * `ACCT`
* **Number:** 
    * `string`
    * e.g.
        * `"1500"`
        * `"4250"`
* **Name:**
    * `string`
    * e.g.
        * `Software Design V`
* **Semesters Offered:**
    * `List<SemesterOffered (enum)>`
    * Enum Keys:
        * `S` - Summer
        * `F` - Fall
        * `W` - Winter
        * `U` - Undefined
    * e.g.
        * `{ S }`
        * `{ S, F, W }`
        * `{ U }`
* **Lecture Hours:** 
    * `float`
    * e.g.
        * `3.0`
        * `5.5`
* **Lab Hours:** 
    * `float`
    * e.g.
        * `6.0`
        * `10.5`
* **Credits:**
    * `float`
    * e.g.
        * `0.5`
        * `0.75`
        * `1.0`
* **Description:**
    * `string`
    * Usually ~50-100 words.
    * e.g.
        * `"This introductory course is designed to..."`
* **Distance Education: (Offerings)** 
    * `DistanceEducation (enum)`
    * Enum Keys:
        * `SUPPLEMENTARY` (in addition to) = `"Also offered through Distance Education format."`
        * `ONLY` (only DE) = `"Offered through Distance Education format only."`
        * `NO` (no DE) = If either of the above are not specified.
    * e.g.
        * `SUPPLEMENTARY`
        * `ONLY`
        * `NO`
* **Year Parity Restrictions: (Offerings)** 
    * `YearParityRestrictions (enum)`
    * Enum Keys:
        * `EVEN_YEARS` = `"Offered in even-numbered years."`
        * `ODD_YEARS` = `"Offered in odd-numbered years."`
        * `NONE` = If either of the above are not specified.
    * e.g. 
        * `EVEN_YEARS`
        * `ODD_YEARS`
        * `NONE`
* **Other (Offerings):**
    * `string`
    * Anything not covered under Distance Education or Year Parity Restrictions.
    * e.g.
        * `"Last offering - Winter 2021"`
* **Prerequisites:**
    * Temporarily: `string`
    * Future:
        * `List<Prerequisite>`
        * A list of `Prerequisite` objects, see below for an explanation.
* **Corequisites:**
    * Temporarily: `string`
    * Future:
        * TBD
* **Equates:**
    * Temporarily: `string`
    * Future:
        * TBD
* **Restrictions:**
    * Temporarily: `string`
    * Future:
        * TBD


### Prerequisite

The `Prerequisite` objects functions in the following way:

`Enum : PrerequisiteState`:
* `Regular`
* `Optional`
* `Any`

`Prerequisite`:
* `courses: List<Course>` = `Courses` this `Prerequisite` object applies to
* `prerequisites: List<Prerequisite>` = other `Prerequisite` objects this `Prerequisite` object applies to
* `state: PrerequisiteState` = one of the above enum states
* `anyAmount: int` = 0 if `PrerequisiteState` is not `Any`, 1-n if `Any`
* `other: string` = If the prerequisites listed from the course aren't divisible into individual courses (e.g. `"All Phase 3 courses"`, `"4.00 credits including X-course"`).

`Prerequisite` objects are then stored in a `List<Prerequisite>` on the `Course` that they apply to.

Each `Prerequisite` object would be broken down until all of the `Courses` in them have the same predicate/logical state.

If a prerequisite has the `other` variable filled, the prerequisite will have to be manually verified (unless we store a list of all potential situations (e.g. have a list of all Phase 3 courses, or a value for the student's total credits accumulated)).

#### Example:
If a course had the following prerequisites:
* A course
* B course or (2 of C, D, E courses)
* F course optional

The `List<Prerequisite>` on the `Course` would look like:
* **1** - Prerequisite(
    &emsp; courses: { A }, 
    &emsp; prerequisites: { }, 
    &emsp; state: Regular, 
    &emsp; anyAmount: 0)
* **2** - Prerequisite(
    &emsp; courses: { B }, 
    &emsp; prerequisites: { 
        &emsp; &emsp; **3** - Prerequisite(
            &emsp; &emsp; &emsp; courses: { C, D, E }, 
            &emsp; &emsp; &emsp; prerequisites: { }, 
            &emsp; &emsp; &emsp; state: Any, 
            &emsp; &emsp; &emsp; anyAmount: 2) }, 
    &emsp; state: Any, 
    &emsp; anyAmount: 1)
* **4** - Prerequisite(
    &emsp; courses: { F }, 
    &emsp; prerequisites: { }, 
    &emsp; state: Optional, 
    &emsp; anyAmount: 0)

Where:
* Prerequisite 1 is just a regular prerequisite where the course(s) (A in this case) are just required like usual, so if you have A the object will collapse into True, otherwise False.
* Prerequisite 2 is a _compound prerequisite_ where if you have B, that fulfils the "Any 1" requirements and Prerequisite 3 doesn't matter, collapsing the prerequisite into True. However, if not it will look at Prerequisite 3 which is a group of courses (C, D, E). If you have "Any 2" of those courses, then the whole compound prerequisite will collapse into True, but if not Prerequisite 2 and 3 will be False.
* Prerequisite 4 is an optional prerequisite so it doesn't actually matter for the calculation of prerequisites.
