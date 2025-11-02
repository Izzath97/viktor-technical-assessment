# SQL Queries - Overview

## Assignment Summary

This section contains SQL solutions for a company/project/employee database system. The database tracks companies, their projects, employees, and project assignments.

## Database Schema

The database consists of four main tables:

1. **Companies** - Stores company information
2. **Projects** - Stores projects with status (running, finished, etc.)
3. **Employees** - Stores employee information
4. **ProjectAssignments** - Many-to-many relationship between employees and projects

See `schema.sql` for the complete database schema with relationships.

## Queries Implemented

### Query 1: Get the names of running Projects
**Objective:** Retrieve all project names that are currently in 'running' status.

**Approach:** Simple SELECT with WHERE clause filtering by status.

**Key Points:**
- Straightforward query focusing only on the Projects table
- Filters by status = 'running'
- Returns only the project names

---

### Query 2: Get the number of finished Projects per Company
**Objective:** Count how many finished projects each company has.

**Approach:** Use LEFT JOIN to include all companies, even those with zero finished projects.

**Key Points:**
- LEFT JOIN ensures all companies appear in results
- Filters projects by status = 'finished' in the JOIN condition
- Groups by company and counts projects
- Orders by count (descending) and company name (ascending)
- Companies with no finished projects show count of 0

**Why LEFT JOIN?**
Using `LEFT JOIN` with the status filter in the ON clause (not WHERE) ensures that:
- All companies appear in the result set
- Companies without finished projects show count = 0
- More informative output for reporting purposes

---

### Query 3: Get Company Names that have 2 or more different Projects with the same Name
**Objective:** Find companies where at least one project name appears 2+ times.

**Approach:** Group by company and project name, then filter with HAVING clause.

**Key Points:**
- JOIN Companies with Projects
- GROUP BY company_id, company_name, AND project_name
- HAVING COUNT(p.id) >= 2 filters project names appearing 2+ times
- DISTINCT ensures each company appears only once
- A company qualifies if ANY of its project names appears multiple times

**Example Scenario:**
```
Company A:
  - Project "Website" (id=1)
  - Project "Website" (id=2)
  - Project "Mobile" (id=3)

Company B:
  - Project "API" (id=4)
  - Project "Dashboard" (id=5)

Result: Company A (has "Website" appearing twice)
```

## SQL Dialect Compatibility

The queries are written to be compatible with:
- **PostgreSQL** (primary target)
- **MySQL** (with minor syntax adjustments)
- **SQLite** (for testing)

### Differences to Note:
- **MySQL:** Uses `AUTO_INCREMENT` for primary keys
- **PostgreSQL:** Uses `SERIAL` or `BIGSERIAL`
- **Date Functions:** May vary between databases

## Testing

Sample test data is included in `queries.sql` (commented out). To test:

1. Create the tables using `schema.sql`
2. Uncomment and run the INSERT statements in `queries.sql`
3. Execute each query and verify results

### Expected Test Results:

**Query 1 Output:**
```
name
-----------------
Website Redesign
API Gateway
Analytics
```

**Query 2 Output:**
```
company_name    | finished_projects_count
----------------|------------------------
TechCorp        | 2
DataSystems     | 1
CloudVentures   | 1
```

**Query 3 Output:**
```
company_name
--------------
CloudVentures
TechCorp
```

## Performance Considerations

1. **Indexes:** The schema includes indexes on:
   - `company_id` and `status` in Projects (composite index)
   - `status` in Projects (for Query 1)
   - Foreign keys (for JOIN operations)

2. **Query Optimization:**
   - Query 1: Index on status enables fast filtering
   - Query 2: Composite index on (company_id, status) optimizes the JOIN + WHERE
   - Query 3: Indexes on company_id enable efficient grouping

3. **Scalability:**
   - All queries use proper indexing strategies
   - GROUP BY uses indexed columns
   - No subqueries or complex nested queries that could cause performance issues

## Alternative Approaches

Each query includes alternative SQL approaches in the comments:
- Different JOIN types (INNER vs LEFT)
- Subquery alternatives
- Additional columns for more detailed output

These alternatives demonstrate different SQL techniques and trade-offs.

---

**Note:** All queries focus on correctness and returning the expected results as specified in the assignment requirements.
