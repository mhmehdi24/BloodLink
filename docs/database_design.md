# Phase 1: Database Design & Normalization (3NF)

## 1. Project Entities & Core Tables

- **Donor**: DonorID (PK), FullName, BloodType, ContactNumber, LastDonationDate
- **BloodBank**: BankID (PK), BankName, Location, ContactNumber
- **BloodInventory**: UnitID (PK), BankID (FK), BloodType, Status, ExpiryDate
- **Donation**: DonationID (PK), DonorID (FK), BankID (FK), DonationDate, VolumeML
- **BloodRequest**: RequestID (PK), HospitalName, BloodType, UnitsRequired, Status, RequestDate

## 2. Relational Integrity Rules

- One `Donor` can have multiple `Donation` records (1:N).
- One `BloodBank` stores multiple `BloodInventory` units and logs multiple `Donation` events (1:N).
- `BloodInventory` units map strictly to valid donor groups via foreign key constraints.

## 3. Normalization Verification (3NF)

- **1NF**: Every field is atomic; no multi-valued blood records or composite attributes exist.
- **2NF**: Fully functional dependencies on primary keys with zero partial dependencies.
- **3NF**: No transitive dependencies across entities.
