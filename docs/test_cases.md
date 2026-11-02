# BloodLink — Test Cases

**Author:** Mahmudul Hasan Mehdi (251-115-028)  
**Date:** 2 November 2026  
**Status:** All passed

---

## Purpose

This document verifies that all 5 business rules (BR-1 through BR-5) are correctly enforced by the BloodLink backend.

Each test was executed against the live API at `http://127.0.0.1:5000` using real database data.

---

## Test 1 — BR-1: 120-Day Donor Recovery Rule

**Endpoint:** `POST /api/donors`

**Scenario:** Attempt to register a new donor whose last donation was only 32 days ago.

**Request body:**

```json
{
  "FullName": "Test Donor Recent",
  "BloodType": "O+",
  "ContactNumber": "01799990001",
  "DateOfBirth": "1995-01-01",
  "Gender": "Male",
  "LastDonationDate": "2026-10-01"
}
```
