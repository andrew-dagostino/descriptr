# UoG Course Descriptr.ly

## Requirements

- [Python 3](https://www.python.org/download/releases/3.0/)
- `pdftotext` v0.62.0

### Installation

1. Install `pdftotext` by installing `poppler-utils` with the following command:

    ```
    apt install poppler-utils
    ```

## Running

## Testing

Unit tests can be run with the following command while in the root directory:

```
python3 -m unittest
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
    * `int`
    * e.g.
        * `1500`
        * `4250`
* **Name:**
    * `string`
    * e.g.
        * `Software Design V`
* **Semesters Offered:**
    * `List<enum>`
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
    * `int`
    * e.g.
        * `3`
* **Lab Hours:** 
    * `int`
    * e.g.
        * `6`
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
    * `enum`
    * Enum Keys:
        * `Supplementary` (in addition to) = `"Also offered through Distance Education format."`
        * `Only` (only DE) = `"Offered through Distance Education format only."`
        * `No` (no DE) = If either of the above are not specified.
    * e.g.
        * `Supplementary`
        * `Only`
        * `No`
* **Year Parity Restrictions: (Offerings)** 
    * `enum`
    * Enum Keys:
        * `Even Years` = `"Offered in even-numbered years."`
        * `Odd Years` = `"Offered in odd-numbered years."`
        * `None` = If either of the above are not specified.
    * e.g. 
        * `Even Years`
        * `Odd Years`
        * `None`
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