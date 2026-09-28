-- ============================================================
-- BloodLink — Core Tables
-- File: 01_core_tables.sql
-- Target: MySQL 8.0+
-- Purpose: Create core entity tables (Hospitals first)
-- ============================================================

CREATE DATABASE IF NOT EXISTS bloodlink_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE bloodlink_db;

-- ------------------------------------------------------------
-- Table: Hospitals
-- External hospitals that submit blood requisitions.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Hospitals (
    HospitalID     INT AUTO_INCREMENT PRIMARY KEY,
    HospitalName   VARCHAR(150) NOT NULL,
    Location       VARCHAR(255) NOT NULL,
    ContactPerson  VARCHAR(100) NOT NULL,
    ContactNumber  VARCHAR(20)  NOT NULL,
    CreatedAt      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);