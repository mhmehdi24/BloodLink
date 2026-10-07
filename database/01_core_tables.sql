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

-- ------------------------------------------------------------
-- Table: Donors
-- Individuals who donate blood. Clinical eligibility is checked
-- at intake (120-day rule) before a new donation is accepted.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Donors (
    DonorID          INT AUTO_INCREMENT PRIMARY KEY,
    FullName         VARCHAR(100) NOT NULL,
    BloodType        ENUM('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
    ContactNumber    VARCHAR(20)  NOT NULL UNIQUE,
    DateOfBirth      DATE         NOT NULL,
    Gender           ENUM('Male','Female','Other') NOT NULL,
    LastDonationDate DATE         NULL,
    CreatedAt        TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Table: Clinical_Records
-- Medical prerequisite measurements recorded at each donor
-- intake visit. One donor can have many records.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Clinical_Records (
    RecordID         INT AUTO_INCREMENT PRIMARY KEY,
    DonorID          INT          NOT NULL,
    RecordDate       DATE         NOT NULL,
    HemoglobinLevel  DECIMAL(4,1) NOT NULL,
    BloodPressure    VARCHAR(10)  NOT NULL,
    WeightKG         DECIMAL(5,2) NOT NULL,
    IsEligible       BOOLEAN      NOT NULL DEFAULT FALSE,
    CreatedAt        TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_clinical_donor
        FOREIGN KEY (DonorID)
        REFERENCES Donors(DonorID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- ------------------------------------------------------------
-- Table: Blood_Inventory
-- Individual physical blood bags. Tracks 42-day expiry and
-- soft-delete status for audit trail.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Blood_Inventory (
    UnitID           INT AUTO_INCREMENT PRIMARY KEY,
    BagCode          VARCHAR(30)  NOT NULL UNIQUE,
    BloodType        ENUM('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
    DonorID          INT          NULL,
    CollectionDate   DATE         NOT NULL,
    ExpiryDate       DATE         NOT NULL,
    Status           ENUM('Active','Dispatched','Discarded') NOT NULL DEFAULT 'Active',
    StorageLocation  VARCHAR(50)  NULL,
    CreatedAt        TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_inventory_donor
        FOREIGN KEY (DonorID)
        REFERENCES Donors(DonorID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- ------------------------------------------------------------
-- Table: Patient_Cases
-- Specific patient blood requirements. Supports Directed
-- Donation: linking one donor's unit to a specific patient.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Patient_Cases (
    CaseID           INT AUTO_INCREMENT PRIMARY KEY,
    PatientName      VARCHAR(100) NOT NULL,
    BloodTypeNeeded  ENUM('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
    UnitsRequired    INT          NOT NULL,
    DirectedDonorID  INT          NULL,
    Status           ENUM('Open','Fulfilled','Cancelled') NOT NULL DEFAULT 'Open',
    OpenedAt         TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_patient_units
        CHECK (UnitsRequired > 0),
    CONSTRAINT fk_patient_donor
        FOREIGN KEY (DirectedDonorID)
        REFERENCES Donors(DonorID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- ------------------------------------------------------------
-- Table: Hospital_Requisitions
-- Emergency blood requests submitted by external hospitals.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Hospital_Requisitions (
    RequisitionID    INT AUTO_INCREMENT PRIMARY KEY,
    HospitalID       INT          NOT NULL,
    BloodTypeNeeded  ENUM('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
    UnitsRequired    INT          NOT NULL,
    UrgencyLevel     ENUM('Standard','Urgent','Critical') NOT NULL DEFAULT 'Standard',
    Status           ENUM('Pending','Approved','Fulfilled','Rejected') NOT NULL DEFAULT 'Pending',
    RequestedAt      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_req_units
        CHECK (UnitsRequired > 0),
    CONSTRAINT fk_req_hospital
        FOREIGN KEY (HospitalID)
        REFERENCES Hospitals(HospitalID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);