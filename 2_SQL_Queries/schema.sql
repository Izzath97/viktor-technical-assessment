-- ============================================================================
-- DATABASE SCHEMA REFERENCE
-- ============================================================================
-- This file contains the database schema for the company/project/employee
-- management system used in the SQL queries assignment.
-- ============================================================================

-- Companies Table
-- Stores information about companies
CREATE TABLE Companies (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Projects Table
-- Stores information about projects belonging to companies
CREATE TABLE Projects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    company_id INT NOT NULL,
    status VARCHAR(50) NOT NULL,
    -- status can be: 'pending', 'running', 'finished', 'cancelled'
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES Companies(id) ON DELETE CASCADE,
    INDEX idx_company_status (company_id, status),
    INDEX idx_status (status)
);

-- Employees Table
-- Stores information about employees working for companies
CREATE TABLE Employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    company_id INT NOT NULL,
    email VARCHAR(255) UNIQUE,
    position VARCHAR(100),
    hire_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES Companies(id) ON DELETE CASCADE,
    INDEX idx_company (company_id)
);

-- ProjectAssignments Table (Join Table)
-- Many-to-many relationship between Employees and Projects
CREATE TABLE ProjectAssignments (
    employee_id INT NOT NULL,
    project_id INT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(100),
    -- role can be: 'Developer', 'Manager', 'Designer', 'QA', etc.
    PRIMARY KEY (employee_id, project_id),
    FOREIGN KEY (employee_id) REFERENCES Employees(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES Projects(id) ON DELETE CASCADE,
    INDEX idx_project (project_id),
    INDEX idx_employee (employee_id)
);

-- ============================================================================
-- SCHEMA DIAGRAM
-- ============================================================================
--
--  ┌─────────────┐
--  │  Companies  │
--  ├─────────────┤
--  │ id (PK)     │
--  │ name        │
--  └──────┬──────┘
--         │
--         │ 1:N
--         │
--    ┌────┴────┬──────────────┐
--    │         │              │
--    │         │              │
-- ┌──▼──────┐  │      ┌───────▼────┐
-- │Projects │  │      │ Employees  │
-- ├─────────┤  │      ├────────────┤
-- │id (PK)  │  │      │ id (PK)    │
-- │name     │  │      │ name       │
-- │comp_id  │  │      │ company_id │
-- │status   │  │      │ email      │
-- └────┬────┘  │      └─────┬──────┘
--      │       │            │
--      │       │            │
--      │  N:M  │            │
--      │   ┌───┴────────┐   │
--      └───►ProjectAssi ◄───┘
--          │gnments     │
--          ├────────────┤
--          │employee_id │
--          │project_id  │
--          │(PK)        │
--          └────────────┘
--
-- ============================================================================

-- Relationships:
-- 1. One Company has many Projects (1:N)
-- 2. One Company has many Employees (1:N)
-- 3. Many Employees can be assigned to many Projects (N:M via ProjectAssignments)
