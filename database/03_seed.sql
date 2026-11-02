-- ============================================================
-- BloodLink — Seed Data
-- File: 03_seed.sql
-- Purpose: Populate database with realistic demo data
-- Idempotent: safe to re-run (uses DELETE first)
-- ============================================================

USE bloodlink_db;

-- Clear existing data (in correct order due to FKs)
DELETE FROM Hospital_Requisitions;
DELETE FROM Patient_Cases;
DELETE FROM Blood_Inventory;
DELETE FROM Clinical_Records;
DELETE FROM Donors;
DELETE FROM Hospitals;

-- Reset auto-increment counters
ALTER TABLE Donors AUTO_INCREMENT = 1;
ALTER TABLE Blood_Inventory AUTO_INCREMENT = 1;
ALTER TABLE Patient_Cases AUTO_INCREMENT = 1;
ALTER TABLE Hospital_Requisitions AUTO_INCREMENT = 1;
ALTER TABLE Clinical_Records AUTO_INCREMENT = 1;
ALTER TABLE Hospitals AUTO_INCREMENT = 1;

-- ------------------------------------------------------------
-- Hospitals (5)
-- ------------------------------------------------------------
INSERT INTO Hospitals (HospitalName, Location, ContactPerson, ContactNumber) VALUES
('Apollo Hospital', 'Dhanmondi, Dhaka', 'Mr. Rahman', '01712345678'),
('Square Hospital', 'Panthapath, Dhaka', 'Ms. Akter', '01798765432'),
('Dhaka Medical College', 'Bakshi Bazar, Dhaka', 'Dr. Hossain', '01711112222'),
('United Hospital', 'Gulshan, Dhaka', 'Mr. Karim', '01733334444'),
('Evercare Hospital', 'Bashundhara, Dhaka', 'Ms. Fatima', '01755556666');

-- ------------------------------------------------------------
-- Donors (30) — varied blood types, some recent, some old
-- ------------------------------------------------------------
INSERT INTO Donors (FullName, BloodType, ContactNumber, DateOfBirth, Gender, LastDonationDate) VALUES
('Karim Ahmed',       'O+',  '01711111101', '1995-06-12', 'Male',   '2026-03-15'),
('Fatima Rahman',     'A+',  '01711111102', '1998-11-03', 'Female', NULL),
('Rashed Khan',       'B+',  '01711111103', '1990-02-20', 'Male',   '2026-06-01'),
('Sadia Islam',       'AB+', '01711111104', '2000-01-01', 'Female', '2026-08-10'),
('Tanvir Hasan',      'O-',  '01711111105', '1993-05-15', 'Male',   '2026-04-20'),
('Nusrat Jahan',      'A-',  '01711111106', '1997-09-22', 'Female', '2026-07-15'),
('Imran Chowdhury',   'B-',  '01711111107', '1988-12-30', 'Male',   NULL),
('Ayesha Siddiqua',   'AB-', '01711111108', '1999-03-18', 'Female', '2026-05-05'),
('Faisal Mahmud',     'O+',  '01711111109', '1994-07-07', 'Male',   '2026-02-28'),
('Rumana Haque',      'A+',  '01711111110', '1996-10-14', 'Female', '2026-09-01'),
('Shakib Al Hasan',   'B+',  '01711111111', '1991-04-25', 'Male',   '2026-01-15'),
('Tasnim Rahman',     'AB+', '01711111112', '2001-08-08', 'Female', NULL),
('Mehedi Hasan',      'O-',  '01711111113', '1992-11-11', 'Male',   '2026-06-20'),
('Farhana Akter',     'A-',  '01711111114', '1995-02-14', 'Female', '2026-08-25'),
('Rakib Hossain',     'B-',  '01711111115', '1989-09-09', 'Male',   '2026-03-30'),
('Sharmin Sultana',   'AB-', '01711111116', '1998-06-06', 'Female', NULL),
('Habib Rahman',      'O+',  '01711111117', '1993-01-20', 'Male',   '2026-07-10'),
('Mitu Islam',        'A+',  '01711111118', '2000-12-12', 'Female', '2026-05-15'),
('Arif Khan',         'B+',  '01711111119', '1987-03-03', 'Male',   '2026-04-01'),
('Nadia Sultana',     'AB+', '01711111120', '1996-07-07', 'Female', NULL),
('Sabbir Ahmed',      'O-',  '01711111121', '1994-10-10', 'Male',   '2026-08-20'),
('Rubina Begum',      'A-',  '01711111122', '1991-05-25', 'Female', '2026-06-05'),
('Jahid Hasan',       'B-',  '01711111123', '1993-12-15', 'Male',   '2026-09-10'),
('Moushumi Akter',    'AB-', '01711111124', '1999-09-19', 'Female', '2026-02-10'),
('Salman Farsi',      'O+',  '01711111125', '1992-08-08', 'Male',   '2026-07-25'),
('Tahmina Rahman',    'A+',  '01711111126', '1997-04-04', 'Female', '2026-03-20'),
('Rafiq Islam',       'B+',  '01711111127', '1990-11-11', 'Male',   '2026-05-30'),
('Samira Khan',       'AB+', '01711111128', '2001-01-25', 'Female', NULL),
('Mizanur Rahman',    'O-',  '01711111129', '1986-06-30', 'Male',   '2026-09-15'),
('Fariha Noor',       'A-',  '01711111130', '1998-03-12', 'Female', '2026-04-18');

-- ------------------------------------------------------------
-- Clinical_Records (15) — for the first 15 donors
-- ------------------------------------------------------------
INSERT INTO Clinical_Records (DonorID, RecordDate, HemoglobinLevel, BloodPressure, WeightKG, IsEligible) VALUES
(1,  '2026-03-15', 14.5, '120/80', 72.5, TRUE),
(2,  '2026-08-10', 13.2, '118/76', 58.0, TRUE),
(3,  '2026-06-01', 15.1, '122/82', 78.3, TRUE),
(4,  '2026-08-10', 12.8, '115/75', 55.2, TRUE),
(5,  '2026-04-20', 14.9, '125/85', 80.1, TRUE),
(6,  '2026-07-15', 13.5, '119/78', 62.5, TRUE),
(7,  '2026-06-10', 14.2, '121/79', 75.8, TRUE),
(8,  '2026-05-05', 13.8, '117/77', 60.3, TRUE),
(9,  '2026-02-28', 15.3, '124/83', 82.4, TRUE),
(10, '2026-09-01', 13.1, '116/74', 57.6, TRUE),
(11, '2026-01-15', 14.7, '123/81', 77.2, TRUE),
(12, '2026-07-20', 12.9, '114/72', 54.8, TRUE),
(13, '2026-06-20', 15.0, '126/86', 79.5, TRUE),
(14, '2026-08-25', 13.4, '118/76', 59.1, TRUE),
(15, '2026-03-30', 14.6, '122/80', 74.2, TRUE);

-- ------------------------------------------------------------
-- Blood_Inventory (50) — mix of Active, Dispatched, Discarded
-- ------------------------------------------------------------
INSERT INTO Blood_Inventory (BagCode, BloodType, DonorID, CollectionDate, ExpiryDate, Status, StorageLocation) VALUES
-- Active (30 bags) — various ages for FIFO testing
('BAG-1001', 'O+',  1,  '2026-10-15', '2026-11-26', 'Active', 'Fridge A - Shelf 1'),
('BAG-1002', 'O+',  9,  '2026-10-20', '2026-12-01', 'Active', 'Fridge A - Shelf 1'),
('BAG-1003', 'O+',  17, '2026-10-25', '2026-12-06', 'Active', 'Fridge A - Shelf 2'),
('BAG-1004', 'A+',  2,  '2026-10-10', '2026-11-21', 'Active', 'Fridge A - Shelf 2'),
('BAG-1005', 'A+',  10, '2026-10-18', '2026-11-29', 'Active', 'Fridge A - Shelf 3'),
('BAG-1006', 'A+',  18, '2026-10-22', '2026-12-03', 'Active', 'Fridge A - Shelf 3'),
('BAG-1007', 'A+',  26, '2026-10-26', '2026-12-07', 'Active', 'Fridge B - Shelf 1'),
('BAG-1008', 'B+',  3,  '2026-10-12', '2026-11-23', 'Active', 'Fridge B - Shelf 1'),
('BAG-1009', 'B+',  11, '2026-10-19', '2026-11-30', 'Active', 'Fridge B - Shelf 2'),
('BAG-1010', 'B+',  19, '2026-10-24', '2026-12-05', 'Active', 'Fridge B - Shelf 2'),
('BAG-1011', 'B+',  27, '2026-10-27', '2026-12-08', 'Active', 'Fridge B - Shelf 3'),
('BAG-1012', 'AB+', 4,  '2026-10-14', '2026-11-25', 'Active', 'Fridge B - Shelf 3'),
('BAG-1013', 'AB+', 12, '2026-10-21', '2026-12-02', 'Active', 'Fridge C - Shelf 1'),
('BAG-1014', 'AB+', 20, '2026-10-25', '2026-12-06', 'Active', 'Fridge C - Shelf 1'),
('BAG-1015', 'O-',  5,  '2026-10-11', '2026-11-22', 'Active', 'Fridge C - Shelf 2'),
('BAG-1016', 'O-',  13, '2026-10-17', '2026-11-28', 'Active', 'Fridge C - Shelf 2'),
('BAG-1017', 'O-',  21, '2026-10-23', '2026-12-04', 'Active', 'Fridge C - Shelf 3'),
('BAG-1018', 'O-',  29, '2026-10-27', '2026-12-08', 'Active', 'Fridge C - Shelf 3'),
('BAG-1019', 'A-',  6,  '2026-10-13', '2026-11-24', 'Active', 'Fridge D - Shelf 1'),
('BAG-1020', 'A-',  14, '2026-10-20', '2026-12-01', 'Active', 'Fridge D - Shelf 1'),
('BAG-1021', 'A-',  22, '2026-10-26', '2026-12-07', 'Active', 'Fridge D - Shelf 2'),
('BAG-1022', 'B-',  7,  '2026-10-16', '2026-11-27', 'Active', 'Fridge D - Shelf 2'),
('BAG-1023', 'B-',  15, '2026-10-22', '2026-12-03', 'Active', 'Fridge D - Shelf 3'),
('BAG-1024', 'B-',  23, '2026-10-26', '2026-12-07', 'Active', 'Fridge D - Shelf 3'),
('BAG-1025', 'AB-', 8,  '2026-10-15', '2026-11-26', 'Active', 'Fridge E - Shelf 1'),
('BAG-1026', 'AB-', 16, '2026-10-21', '2026-12-02', 'Active', 'Fridge E - Shelf 1'),
('BAG-1027', 'AB-', 24, '2026-10-27', '2026-12-08', 'Active', 'Fridge E - Shelf 2'),
('BAG-1028', 'O+',  25, '2026-10-28', '2026-12-09', 'Active', 'Fridge E - Shelf 2'),
('BAG-1029', 'A+',  30, '2026-10-28', '2026-12-09', 'Active', 'Fridge E - Shelf 3'),
('BAG-1030', 'B+',  28, '2026-10-28', '2026-12-09', 'Active', 'Fridge E - Shelf 3'),
-- Dispatched (12 bags)
('BAG-2001', 'O+',  1,  '2026-09-15', '2026-10-27', 'Dispatched', 'Sent to Apollo'),
('BAG-2002', 'A+',  2,  '2026-09-20', '2026-11-01', 'Dispatched', 'Sent to Square'),
('BAG-2003', 'B+',  3,  '2026-09-25', '2026-11-06', 'Dispatched', 'Sent to DMCH'),
('BAG-2004', 'AB+', 4,  '2026-09-28', '2026-11-09', 'Dispatched', 'Sent to United'),
('BAG-2005', 'O-',  5,  '2026-09-30', '2026-11-11', 'Dispatched', 'Sent to Evercare'),
('BAG-2006', 'A-',  6,  '2026-10-01', '2026-11-12', 'Dispatched', 'Sent to Apollo'),
('BAG-2007', 'B-',  7,  '2026-10-05', '2026-11-16', 'Dispatched', 'Sent to Square'),
('BAG-2008', 'AB-', 8,  '2026-10-07', '2026-11-18', 'Dispatched', 'Sent to DMCH'),
('BAG-2009', 'O+',  9,  '2026-10-08', '2026-11-19', 'Dispatched', 'Sent to United'),
('BAG-2010', 'A+',  10, '2026-10-10', '2026-11-21', 'Dispatched', 'Sent to Evercare'),
('BAG-2011', 'B+',  11, '2026-10-12', '2026-11-23', 'Dispatched', 'Sent to Apollo'),
('BAG-2012', 'O-',  13, '2026-10-14', '2026-11-25', 'Dispatched', 'Sent to Square'),
-- Discarded (8 bags) — expired / compromised
('BAG-3001', 'O+',  1,  '2026-08-15', '2026-09-26', 'Discarded', 'Quarantine'),
('BAG-3002', 'A+',  2,  '2026-08-20', '2026-10-01', 'Discarded', 'Quarantine'),
('BAG-3003', 'B+',  3,  '2026-08-25', '2026-10-06', 'Discarded', 'Quarantine'),
('BAG-3004', 'AB+', 4,  '2026-09-01', '2026-10-13', 'Discarded', 'Quarantine'),
('BAG-3005', 'O-',  5,  '2026-09-05', '2026-10-17', 'Discarded', 'Quarantine'),
('BAG-3006', 'A-',  6,  '2026-09-10', '2026-10-22', 'Discarded', 'Quarantine'),
('BAG-3007', 'B-',  7,  '2026-09-15', '2026-10-27', 'Discarded', 'Quarantine'),
('BAG-3008', 'AB-', 8,  '2026-09-20', '2026-11-01', 'Discarded', 'Quarantine');

-- ------------------------------------------------------------
-- Patient_Cases (15)
-- ------------------------------------------------------------
INSERT INTO Patient_Cases (PatientName, BloodTypeNeeded, UnitsRequired, DirectedDonorID, Status, OpenedAt) VALUES
('Ayesha Khan',      'O+',  2, 1,    'Open',      '2026-10-28 09:30:00'),
('Mohammed Ali',     'A+',  3, NULL, 'Open',      '2026-10-28 10:15:00'),
('Rokeya Begum',     'B+',  1, NULL, 'Fulfilled', '2026-10-27 14:20:00'),
('Shahid Islam',     'O-',  2, 5,    'Open',      '2026-10-28 08:00:00'),
('Nargis Akter',     'AB+', 4, NULL, 'Open',      '2026-10-28 11:45:00'),
('Kamal Hossain',    'A-',  1, NULL, 'Fulfilled', '2026-10-27 16:30:00'),
('Sultana Razia',    'B-',  2, NULL, 'Open',      '2026-10-28 07:20:00'),
('Enamul Haque',     'AB-', 1, 8,    'Open',      '2026-10-28 12:00:00'),
('Taslima Khatun',   'O+',  3, NULL, 'Cancelled', '2026-10-26 09:00:00'),
('Moinul Islam',     'A+',  2, 10,   'Open',      '2026-10-28 13:30:00'),
('Shirin Sultana',   'B+',  1, NULL, 'Open',      '2026-10-28 14:15:00'),
('Abdul Karim',      'O-',  2, NULL, 'Fulfilled', '2026-10-26 15:00:00'),
('Rumana Haque',     'A-',  3, NULL, 'Open',      '2026-10-28 15:45:00'),
('Sattar Miah',      'AB+', 2, NULL, 'Open',      '2026-10-28 16:20:00'),
('Jasmine Akter',    'B-',  1, 15,   'Open',      '2026-10-28 17:00:00');

-- ------------------------------------------------------------
-- Hospital_Requisitions (10)
-- ------------------------------------------------------------
INSERT INTO Hospital_Requisitions (HospitalID, BloodTypeNeeded, UnitsRequired, UrgencyLevel, Status, RequestedAt) VALUES
(1, 'O+',  3, 'Urgent',   'Pending',  '2026-10-28 08:30:00'),
(2, 'A+',  2, 'Critical', 'Pending',  '2026-10-28 09:15:00'),
(3, 'B+',  5, 'Standard', 'Pending',  '2026-10-27 18:00:00'),
(4, 'O-',  2, 'Critical', 'Pending',  '2026-10-28 10:00:00'),
(5, 'AB+', 4, 'Urgent',   'Pending',  '2026-10-28 11:00:00'),
(1, 'A-',  3, 'Standard', 'Approved', '2026-10-27 14:30:00'),
(2, 'B-',  2, 'Urgent',   'Fulfilled','2026-10-26 13:00:00'),
(3, 'AB-', 1, 'Standard', 'Pending',  '2026-10-28 12:30:00'),
(4, 'O+',  4, 'Critical', 'Pending',  '2026-10-28 13:45:00'),
(5, 'A+',  2, 'Standard', 'Rejected', '2026-10-26 15:30:00');