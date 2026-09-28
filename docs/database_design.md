# BloodLink — Database Design & Normalization (3NF)

**Author:** Mahmudul Hasan Mehdi (251-115-028)  
**Date:** 29 September 2026  
**Status:** Final for v1.0  
**Related files:** `docs/er_diagram.md`, `database/01_core_tables.sql`

---

## 1. Design Goals

BloodLink is a centralized, database-driven blood bank management system.
The database is designed to:

- Enforce medical business rules (120-day donor recovery, 42-day expiry)
  at the **database and backend level**, not by manual check.
- Preserve an **immutable audit trail** using soft-deletes, so wastage
  analytics never lose historical data.
- Support an **algorithmic FIFO dispatch** for matching hospital requests
  to the oldest viable blood units.
- Maintain strict **relational integrity** through primary and foreign keys.

---

## 2. Entity Overview

The schema consists of six tables:

| #   | Table                   | Purpose                                       | Cardinality             |
| --- | ----------------------- | --------------------------------------------- | ----------------------- |
| 1   | `Hospitals`             | External hospitals that submit requisitions   | —                       |
| 2   | `Donors`                | Individuals who donate blood                  | —                       |
| 3   | `Clinical_Records`      | Eligibility check-ups per donor visit         | Donors 1 : N            |
| 4   | `Blood_Inventory`       | Individual physical blood bags                | Donors 1 : N            |
| 5   | `Patient_Cases`         | Patient requirements (with directed donation) | Donors 1 : N (optional) |
| 6   | `Hospital_Requisitions` | Emergency requests from hospitals             | Hospitals 1 : N         |

Full column-level detail is in `docs/er_diagram.md`.

---

## 3. Normalization Verification (3NF)

### 3.1 First Normal Form (1NF)

**Rule:** Every column holds a single, atomic value. No repeating groups, no multi-valued cells.

**Applied:**

- Every column stores one value (e.g. `FullName` = one string, `BloodType` = one ENUM).
- The old-style practice of storing `donor1, donor2, donor3` in a single cell is not used anywhere.
- Clinical measurements are stored one row per visit in `Clinical_Records`, not repeated as columns (`BP1`, `BP2`, `BP3`).

**Verdict:** Schema is in 1NF.

---

### 3.2 Second Normal Form (2NF)

**Rule:** Schema is in 1NF, and every non-key column depends on the **whole** primary key — not just part of it.

**Applied:**

- All tables use a **single-column surrogate primary key** (`DonorID`, `RecordID`, `UnitID`, etc.). There are no composite keys, so partial dependency is impossible.
- No non-key column depends on only part of a key.

**Verdict:** Schema is in 2NF.

---

### 3.3 Third Normal Form (3NF)

**Rule:** Schema is in 2NF, and no non-key column depends transitively on another non-key column.

**Applied:**

- `Donors.BloodType` is stored once, on the donor. It is **not** repeated in `Clinical_Records` or `Blood_Inventory`.
- `Blood_Inventory` carries its own `BloodType` only because a bag is a physical object with its own barcode — it is an independent fact about the bag, not a copy of the donor's type. (This is a deliberate, documented exception: the bag could in theory outlive the donor record or come from an unknown donor.)
- `Hospitals.Location` and `Hospitals.ContactNumber` are stored once on the hospital row, not repeated in every requisition.
- `Clinical_Records.IsEligible` is a snapshot decision per visit — it depends on the record's own data, not on another table.

**Verdict:** Schema is in 3NF.

---

## 4. Integrity Constraints

The following constraints are enforced by the database itself:

| Constraint                            | Where                                                                   | Purpose                              |
| ------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------ |
| Primary keys                          | Every table                                                             | Uniqueness                           |
| `UNIQUE` on `Donors.ContactNumber`    | Donors                                                                  | Prevent duplicate donor registration |
| `UNIQUE` on `Blood_Inventory.BagCode` | Blood_Inventory                                                         | One barcode = one bag                |
| Foreign keys                          | Clinical_Records, Blood_Inventory, Patient_Cases, Hospital_Requisitions | Referential integrity                |
| `CHECK (UnitsRequired > 0)`           | Patient_Cases, Hospital_Requisitions                                    | Reject nonsensical quantities        |
| `ENUM` domains                        | BloodType, Status, UrgencyLevel, etc.                                   | Restrict values to valid set         |

---

## 5. Business Rules Enforced

| Rule                               | Enforced in                                         |
| ---------------------------------- | --------------------------------------------------- |
| **BR-1** — 120-day donor recovery  | Backend (`T3.5`), reads `Donors.LastDonationDate`   |
| **BR-2** — 42-day expiry           | Backend (`T3.7`), sets `Blood_Inventory.ExpiryDate` |
| **BR-3** — FIFO dispatch           | Backend query (`T3.11`), `ORDER BY ExpiryDate ASC`  |
| **BR-4** — Soft-delete audit trail | Backend (`T3.8`), `UPDATE Status = 'Discarded'`     |
| **BR-5** — Directed donation       | `Patient_Cases.DirectedDonorID` foreign key         |

---

## 6. Change Log

| Date        | Change                       | Reason                                                                                                                                                                        |
| ----------- | ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 20 Sep 2026 | Initial draft (5 tables)     | First attempt, old proposal                                                                                                                                                   |
| 29 Sep 2026 | Rewritten for 6-table schema | Aligned with updated proposal; added `Hospitals` and `Clinical_Records`; renamed `BloodRequest` → `Hospital_Requisitions`; added `DirectedDonorID` support to `Patient_Cases` |

The old 5-table version was stored at `database/schema.sql` and has been
superseded. The current schema files live in `database/01_core_tables.sql`
and later numbered files.
