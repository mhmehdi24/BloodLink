# BloodLink — Requirements and Scope Lock

**Version:** 1.0 (MVP Capstone Build)  
**Author:** Mahmudul Hasan Mehdi (251-115-028)  
**Batch:** 62/A  
**Course:** Computer Science & Engineering Capstone  
**Target Defense Date:** 25 November 2026  
**Status:** Locked

---

## 1. Overview

BloodLink is a centralized, database-driven blood bank management application
designed to track the complete medical lifecycle of blood units. Operating
from a single-operator central hub, the system oversees donor triage, physical
blood intake, inventory quarantine, and hospital dispatch.

The project emphasizes strict relational data integrity and automated medical
business rules to streamline operations and reduce biological wastage.

---

## 2. Problem Statement

Traditional or poorly optimized blood bank systems rely on manual tracking
and fragmented data management. This leads to critical inefficiencies:

- **Biological Wastage:** Without automated expiry tracking and FIFO
  dispatching, viable blood units often expire in storage.
- **Medical Rule Violations:** Manual record-keeping fails to consistently
  enforce mandatory donor recovery intervals, risking donor health.
- **Loss of Audit Trails:** Basic databases often permanently delete expired
  or discarded units, destroying historical data needed for wastage analytics
  and supply chain reporting.
- **Inefficient Triage:** Emergency hospital requests are often disconnected
  from real-time active inventory, delaying critical patient care.

---

## 3. Proposed Solution

BloodLink provides a highly normalized, centralized web application that
replaces manual tracking with database-enforced constraints. The system:

- Automatically calculates the exact 42-day expiration for whole blood.
- Algorithmically prioritizes the oldest viable units for dispatch.
- Strictly enforces a 120-day recovery interval for returning donors.
- Uses a "soft-delete" architecture to guarantee an immutable audit trail
  for all discarded units, powering accurate real-time analytics.

---

## 4. Technology Stack

| Layer    | Technology                                                                   |
| -------- | ---------------------------------------------------------------------------- |
| Frontend | Vanilla HTML5, CSS3, JavaScript (ES6) — no framework, direct API consumption |
| Backend  | Python Flask (RESTful API)                                                   |
| Database | MySQL, normalized to 3NF                                                     |
| Tooling  | Git, GitHub, VS Code, MySQL Workbench                                        |

---

## 5. Core Functional Modules

BloodLink operates as a single-operator Central Hub with the following
core modules:

### M0 — Admin Entry Screen (UI only)

- A single cosmetic login screen for the central admin, used as the UI
  entry point for the demo.
- No credentials are validated; no password is stored; no session is
  created. Clicking "Sign In" navigates directly to the dashboard.
- Real authentication and RBAC are explicitly out of scope (see Section 7).

### M1 — Donor Clinical Triage

- Registers donors with clinical prerequisites (blood pressure, weight,
  hemoglobin).
- Automatically rejects intake if the 120-day recovery interval has not
  passed since the donor's last donation.

### M2 — Patient Case Management

- Logs specific patient blood requirements.
- Supports a **Directed Donation** feature that links a specific family
  member's blood unit exclusively to a designated patient.

### M3 — Inventory & Expiry Engine

- Simulates manual barcode entry for physical blood units.
- Automatically generates a 42-day expiry countdown from the collection date.

### M4 — Inbound Hub Request Board

- Central queue for external hospital emergency requests.
- Requests are triaged by clinical urgency.

### M5 — Algorithmic Match & Dispatch

- Cross-matches pending hospital requests with compatible 'Active' inventory.
- Applies a FIFO algorithm (oldest viable units dispatched first) to
  minimize wastage.

### M6 — System Analytics

- Executive dashboard aggregating active stock levels, demand spikes, and
  real-time wastage percentage.
- Wastage is computed from soft-deleted audit records.

---

## 6. Business Rules (Locked)

- **BR-1 — 120-Day Recovery Interval:** The system must reject a new
  donation entry if fewer than 120 days have passed since the donor's last
  recorded donation.
- **BR-2 — 42-Day Expiry Engine:** Every whole blood unit receives an
  expiry date exactly 42 days after its collection date.
- **BR-3 — FIFO Dispatch:** When allocating units to requests, compatible
  units are sorted by `expiry_date ASC` so the oldest viable units are
  dispatched first.
- **BR-4 — Immutable Audit Trail (Soft Deletes):** Expired, compromised,
  or discarded units are never removed using SQL `DELETE`. Their status is
  updated to `'Discarded'`, preserving wastage analytics.
- **BR-5 — Directed Donation:** A directed donation unit may only be
  allocated to the specific patient it was registered for.

---

## 7. Scope Exclusions (Locked for v1.0)

The following features are explicitly excluded from this build phase:

- Multi-user Role-Based Access Control (RBAC) and separate login portals
  for hospitals, patients, or donors.
- Multi-tenant SaaS data isolation.
- Integration with physical ISBT 128 barcode scanning hardware
  (barcodes are simulated via manual text entry).
- Live WebSockets — updates rely on standard REST request/response cycles.

**Clarification:** The admin login screen in M0 is a UI-only entry point
for demonstration. It does not implement authentication, session handling,
or RBAC. All backend routes remain unprotected in v1.0. This is consistent
with the single-operator Central Hub scope.

---

## 8. Non-Functional Requirements

- **NFR-1 Performance:** Common lookups (donor search, inventory list,
  match query) return in under 1 second on realistic mock data.
- **NFR-2 Integrity:** All primary/foreign keys and constraints enforced
  at the database level.
- **NFR-3 Security:** Credentials stored in `.env`, never committed to Git.
- **NFR-4 Usability:** Responsive layout usable on desktop and tablet widths.
- **NFR-5 Maintainability:** Schema, API, and design documented in `docs/`.

---

## 9. Development Milestones

| Phase   | Description                                                 | Status                                            |
| ------- | ----------------------------------------------------------- | ------------------------------------------------- |
| Phase 1 | UI/UX prototyping (7 screens, HTML/JS)                      | Drafted in design tool — pending repo integration |
| Phase 2 | Database architecture (3NF MySQL schema, keys, constraints) | Active                                            |
| Phase 3 | Backend logic (Flask REST API, query optimization)          | Planned                                           |
| Phase 4 | Integration (frontend `fetch()` wired to backend API)       | Planned                                           |
| Phase 5 | Pre-defense audit (bug testing, realistic mock data)        | Planned                                           |

**Hard deadline:** 25 November 2026.

---

## 10. Expected Outcome

A fully functional, bug-free core web application that demonstrates advanced
relational database schema design and backend API integration. The completed
system will provide a visual, interactive proof-of-concept showing how strict
SQL data constraints and algorithmic sorting solve real-world healthcare
supply chain inefficiencies.
