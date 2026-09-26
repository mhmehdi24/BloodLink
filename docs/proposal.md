# BloodLink — Project Proposal

**Developer:** Mahmudul Hasan Mehdi (251-115-028)  
**Course:** Computer Science & Engineering Capstone  
**Target Defense Date:** 25 November 2026  
**Version:** 1.0 (MVP Capstone Build)

---

## Overview

BloodLink is a centralized, database-driven blood bank management application
designed to track the complete medical lifecycle of blood units. Operating
from a single-operator central hub, the system oversees donor triage, physical
blood intake, inventory quarantine, and hospital dispatch. The project
emphasizes strict relational data integrity and automated medical business
rules to streamline operations and reduce biological wastage.

---

## Problem Statement

Traditional or poorly optimized blood bank systems often rely on manual
tracking and fragmented data management. This leads to critical
inefficiencies:

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

## Proposed Solution

BloodLink provides a highly normalized, centralized web application that
replaces manual tracking with database-enforced constraints. The system
automatically calculates the exact 42-day expiration for whole blood,
algorithmically prioritizes the oldest viable units for dispatch, and strictly
enforces a 120-day recovery interval for returning donors. By utilizing a
"soft-delete" architecture, the system guarantees an immutable audit trail
for all discarded units, powering accurate real-time analytics.

---

## Features

- **Donor Clinical Triage:** A donor registration module that logs clinical
  prerequisites (hemoglobin, blood pressure) and automatically rejects intake
  if the 120-day recovery interval is not met.
- **Patient Case Management:** Logs specific patient blood requirements,
  including a "Directed Donation" feature that links a specific family
  member's blood bag exclusively to a designated patient.
- **Inventory & Expiry Engine:** Simulates barcode logging and automatically
  generates a 42-day expiry countdown for physical inventory.
- **Algorithmic Match & Dispatch:** A core logic engine that cross-matches
  pending hospital requests with compatible 'Active' inventory using a FIFO
  algorithm to minimize wastage.
- **System Analytics:** An executive dashboard aggregating active stock
  levels, demand spikes, and real-time wastage percentages based on the
  soft-deleted audit records.

---

## Technical Approach

- **Frontend Environment:** Vanilla HTML5, CSS3, and JavaScript (ES6) to
  demonstrate raw DOM manipulation and direct API consumption without relying
  on abstraction frameworks.
- **Backend Framework:** Python Flask (RESTful API) to handle business logic
  and route data.
- **Database Architecture:** 3NF Normalized MySQL Database utilizing
  optimized queries, relational foreign keys, and status-based updates.

---

## Scope

BloodLink is scoped specifically as a single-environment Central Command Hub
managed by central blood bank operators. To ensure a stable, bug-free
deployment by the project deadline, the following are strictly excluded from
this build:

- Multi-user Role-Based Access Control (RBAC) and separate login portals for
  external hospitals, patients, or donors.
- Multi-tenant SaaS data isolation.
- Integration with physical ISBT 128 barcode scanning hardware (barcodes will
  be simulated via manual text entry).
- Live WebSockets (updates rely on standard REST request/response cycles).

---

## Version

Version 1.0 (MVP Capstone Build)

---

## Expected Outcome

The delivery of a fully functional, bug-free core web application that
successfully demonstrates advanced relational database schema design and
backend API integration. The completed system will provide a visual,
interactive proof-of-concept showing how strict SQL data constraints and
algorithmic sorting can solve real-world healthcare supply chain
inefficiencies.
