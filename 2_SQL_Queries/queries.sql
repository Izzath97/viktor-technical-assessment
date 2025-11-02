-- ============================================================================
-- SQL QUERIES FOR COMPANY/PROJECT/EMPLOYEE DATABASE
-- ============================================================================
-- Author: Mohamed Izzath
-- Date: November 2, 2025
-- Description: Solutions to three SQL queries for analyzing company projects
-- Database: PostgreSQL/MySQL compatible syntax
-- ============================================================================

-- Database Schema Reference:
-- 
-- Companies (id, name)
-- Projects (id, name, company_id, status)
-- Employees (id, name, company_id)
-- ProjectAssignments (employee_id, project_id)
--
-- Assumptions:
-- - status field in Projects table can be: 'running', 'finished', 'pending', etc.
-- - Multiple employees can be assigned to multiple projects (many-to-many)
-- - Companies can have multiple projects with the same name
-- ============================================================================


-- ============================================================================
-- QUERY 1: Get the names of the running Projects
-- ============================================================================
-- Description: Retrieves all project names that are currently in 'running' status
-- Returns: Single column with project names
-- ============================================================================

SELECT name
FROM Projects
WHERE status = 'running';

-- Alternative with more details (if needed):
-- SELECT 
--     p.id,
--     p.name,
--     c.name AS company_name
-- FROM Projects p
-- JOIN Companies c ON p.company_id = c.id
-- WHERE p.status = 'running'
-- ORDER BY p.name;


-- ============================================================================
-- QUERY 2: Get the number of finished Projects per Company
-- ============================================================================
-- Description: Counts how many finished projects each company has
-- Returns: Company names and their count of finished projects
-- Note: Includes companies with 0 finished projects using LEFT JOIN
-- ============================================================================

SELECT 
    c.name AS company_name,
    COUNT(p.id) AS finished_projects_count
FROM Companies c
LEFT JOIN Projects p 
    ON c.id = p.company_id 
    AND p.status = 'finished'
GROUP BY c.id, c.name
ORDER BY finished_projects_count DESC, company_name ASC;

-- Note: The LEFT JOIN ensures all companies appear in results, even if they
-- have no finished projects. Companies with no finished projects will show
-- a count of 0.

-- Alternative (if you only want companies that have finished projects):
-- SELECT 
--     c.name AS company_name,
--     COUNT(p.id) AS finished_projects_count
-- FROM Companies c
-- INNER JOIN Projects p ON c.id = p.company_id
-- WHERE p.status = 'finished'
-- GROUP BY c.id, c.name
-- ORDER BY finished_projects_count DESC;


-- ============================================================================
-- QUERY 3: Get the Company Names that have 2 or more different Projects 
--          with the same Name
-- ============================================================================
-- Description: Finds companies where at least one project name appears 
--              in 2 or more different projects (different IDs)
-- Returns: Company names that meet the criteria
-- ============================================================================

SELECT DISTINCT c.name AS company_name
FROM Companies c
JOIN Projects p ON c.id = p.company_id
GROUP BY c.id, c.name, p.name
HAVING COUNT(p.id) >= 2
ORDER BY c.name;

-- Explanation:
-- 1. JOIN Companies with Projects to get all company-project relationships
-- 2. GROUP BY company AND project name to group projects with same name per company
-- 3. HAVING COUNT(p.id) >= 2 filters to only include project names that appear
--    2 or more times for the same company
-- 4. DISTINCT ensures each company appears only once in results
-- 5. A company qualifies if ANY of its project names appears 2+ times

-- Alternative approach with subquery (more explicit):
-- SELECT DISTINCT c.name AS company_name
-- FROM Companies c
-- WHERE EXISTS (
--     SELECT p1.name
--     FROM Projects p1
--     WHERE p1.company_id = c.id
--     GROUP BY p1.name
--     HAVING COUNT(p1.id) >= 2
-- )
-- ORDER BY c.name;

-- Example data to understand Query 3:
-- Company A has: Project "Alpha" (id=1), Project "Alpha" (id=2), Project "Beta" (id=3)
-- Company B has: Project "Gamma" (id=4), Project "Delta" (id=5)
-- Company C has: Project "Omega" (id=6), Project "Omega" (id=7), Project "Omega" (id=8)
-- 
-- Result: Company A, Company C
-- (Both have at least one project name appearing 2+ times)


-- ============================================================================
-- TESTING QUERIES
-- ============================================================================
-- Sample data for testing (uncomment to test):

/*
-- Create tables
CREATE TABLE Companies (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Projects (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    company_id INT,
    status VARCHAR(50),
    FOREIGN KEY (company_id) REFERENCES Companies(id)
);

CREATE TABLE Employees (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    company_id INT,
    FOREIGN KEY (company_id) REFERENCES Companies(id)
);

CREATE TABLE ProjectAssignments (
    employee_id INT,
    project_id INT,
    PRIMARY KEY (employee_id, project_id),
    FOREIGN KEY (employee_id) REFERENCES Employees(id),
    FOREIGN KEY (project_id) REFERENCES Projects(id)
);

-- Insert sample data
INSERT INTO Companies (id, name) VALUES
(1, 'TechCorp'),
(2, 'DataSystems'),
(3, 'CloudVentures');

INSERT INTO Projects (id, name, company_id, status) VALUES
(1, 'Website Redesign', 1, 'running'),
(2, 'Mobile App', 1, 'finished'),
(3, 'Website Redesign', 1, 'finished'),  -- Duplicate name
(4, 'API Gateway', 2, 'running'),
(5, 'Data Pipeline', 2, 'finished'),
(6, 'Analytics', 3, 'pending'),
(7, 'Analytics', 3, 'running'),  -- Duplicate name
(8, 'Analytics', 3, 'finished'); -- Duplicate name (3 times total)

INSERT INTO Employees (id, name, company_id) VALUES
(1, 'John Doe', 1),
(2, 'Jane Smith', 1),
(3, 'Bob Johnson', 2),
(4, 'Alice Williams', 3);

INSERT INTO ProjectAssignments (employee_id, project_id) VALUES
(1, 1),
(1, 2),
(2, 1),
(3, 4),
(3, 5),
(4, 6),
(4, 7);

-- Test Query 1 (Expected: 'Website Redesign', 'API Gateway', 'Analytics')
SELECT name FROM Projects WHERE status = 'running';

-- Test Query 2 (Expected: TechCorp: 2, DataSystems: 1, CloudVentures: 1)
SELECT c.name, COUNT(p.id) AS finished_projects_count
FROM Companies c
LEFT JOIN Projects p ON c.id = p.company_id AND p.status = 'finished'
GROUP BY c.id, c.name
ORDER BY finished_projects_count DESC;

-- Test Query 3 (Expected: TechCorp, CloudVentures)
SELECT DISTINCT c.name AS company_name
FROM Companies c
JOIN Projects p ON c.id = p.company_id
GROUP BY c.id, c.name, p.name
HAVING COUNT(p.id) >= 2
ORDER BY c.name;
*/
