-- ============================================================
-- BloodLink Database Schema (Phase 2)
-- Architecture: 3NF Relational Model
-- Target DBMS: MySQL 8.0+
-- ============================================================

CREATE DATABASE IF NOT EXISTS bloodlink_db;
USE bloodlink_db;

-- ------------------------------------------------------------
-- 1. Table: Donor
-- Stores voluntary donor details and eligibility tracking.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Donor (
    DonorID INT AUTO_INCREMENT PRIMARY KEY,
    FullName VARCHAR(100) NOT NULL,
    BloodType ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-') NOT NULL,
    ContactNumber VARCHAR(20) NOT NULL UNIQUE,
    LastDonationDate DATE NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- 2. Table: BloodBank
-- Stores regional bank branches holding physical units.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS BloodBank (
    BankID INT AUTO_INCREMENT PRIMARY KEY,
    BankName VARCHAR(120) NOT NULL,
    Location VARCHAR(255) NOT NULL,
    ContactNumber VARCHAR(20) NOT NULL
);-- ------------------------------------------------------------
-- 3. Table: BloodInventory
-- Tracks individual blood bags/units stored across blood banks.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS BloodInventory (
    UnitID INT AUTO_INCREMENT PRIMARY KEY,
    BankID INT NOT NULL,
    BloodType ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-') NOT NULL,
    Status ENUM('Available', 'Reserved', 'Transfused', 'Expired') DEFAULT 'Available',
    CollectedDate DATE NOT NULL,
    ExpiryDate DATE NOT NULL,
    CONSTRAINT fk_inventory_bank
        FOREIGN KEY (BankID) 
        REFERENCES BloodBank(BankID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
-- ------------------------------------------------------------
-- 4. Table: Donation
-- Records individual donation events connecting donors and banks.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS Donation (
    DonationID INT AUTO_INCREMENT PRIMARY KEY,
    DonorID INT NOT NULL,
    BankID INT NOT NULL,
    DonationDate DATE NOT NULL,
    VolumeML INT NOT NULL DEFAULT 450,
    HemoglobinLevel DECIMAL(4, 1) NULL,
    CONSTRAINT fk_donation_donor
        FOREIGN KEY (DonorID)
        REFERENCES Donor(DonorID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_donation_bank
        FOREIGN KEY (BankID)
        REFERENCES BloodBank(BankID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);
-- ------------------------------------------------------------
-- 5. Table: BloodRequest
-- Captures institutional blood requests from hospitals.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS BloodRequest (
    RequestID INT AUTO_INCREMENT PRIMARY KEY,
    HospitalName VARCHAR(150) NOT NULL,
    BloodType ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-') NOT NULL,
    UnitsRequired INT NOT NULL CHECK (UnitsRequired > 0),
    UrgencyLevel ENUM('Standard', 'Urgent', 'Critical') DEFAULT 'Standard',
    Status ENUM('Pending', 'Approved', 'Fulfilled', 'Rejected') DEFAULT 'Pending',
    RequestDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);-- ------------------------------------------------------------
---- ------------------------------------------------------------
-- 