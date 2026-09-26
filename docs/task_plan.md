# BloodLink — Solo Task Plan (v1.0)

**Author:** Mahmudul Hasan Mehdi (251-115-028)  
**Deadline:** 25 November 2026  
**Workload:** ~1 hour/day, solo, no slack  
**Total budget:** ~62 hours

Task numbering: **Phase X.Y** (supersedes old T1–T19).

---

## Phase 1 — Database Architecture · 24 Sep – 03 Oct · ~10 hrs

**Goal:** Lock the 3NF MySQL schema so the backend has a solid foundation.

- [ ] **P1.1** Create core tables (Hospitals, Donors, Clinical_Records) — 2 hrs
- [ ] **P1.2** Create transactional tables (Blood_Inventory, Patient_Cases, Hospital_Requisitions) — 2 hrs
- [ ] **P1.3** Apply constraints & ENUMs (FKs, status enums, `ON DELETE` rules) — 2 hrs
- [ ] **P1.4** Instantiate database in MySQL Workbench; verify with `SHOW TABLES` — 1 hr
- [ ] **P1.5** Draw ER diagram (Mermaid in `docs/er_diagram.md`) — 2 hrs
- [ ] **P1.6** Write `docs/database_design.md` — normalization + table definitions — 1 hr

**Milestone M1 — Schema live** (target: 03 Oct)

---

## Phase 2 — Flask Backend & Business Logic · 04 Oct – 18 Oct · ~15 hrs

**Goal:** REST API endpoints enforcing the medical rules.

- [ ] **P2.1** Virtual env, install Flask, Flask-CORS, PyMySQL, python-dotenv — 1 hr
- [ ] **P2.2** `.env` + `.gitignore` secrets check + DB connection module — 1 hr
- [ ] **P2.3** `/api/donors` GET (search) — 1.5 hrs
- [ ] **P2.4** `/api/donors` POST + **120-day rule** — 2 hrs
- [ ] **P2.5** `/api/inventory` GET (active stock) + POST (new bag) — 1.5 hrs
- [ ] **P2.6** **42-day expiry engine** on bag creation — 1 hr
- [ ] **P2.7** `/api/requests` GET (pending queue) + POST (new emergency) — 2 hrs
- [ ] **P2.8** **FIFO dispatch query** — `ORDER BY expiry_date ASC LIMIT` — 2 hrs
- [ ] **P2.9** `PATCH /api/inventory/:id` for soft-delete (status → 'Discarded') — 1 hr
- [ ] **P2.10** Manual test every endpoint with `curl` or Postman — 2 hrs

**Milestone M2 — API live** (target: 18 Oct)

---

## Phase 3 — Frontend Integration · 19 Oct – 02 Nov · ~15 hrs

**Goal:** Replace static UI with live database data.

- [ ] **P3.1** Move Google AI Studio HTML into `frontend/` — 1 hr
- [ ] **P3.2** Shared `api.js` helper (`get()`, `post()`, `patch()`) — 1 hr
- [ ] **P3.3** Wire S3 (Donor search + register) — 2 hrs
- [ ] **P3.4** Wire S4 (Blood intake + discard/soft-delete) — 2 hrs
- [ ] **P3.5** Wire S2 & S5 (Patient case + hospital requisition forms) — 2 hrs
- [ ] **P3.6** Wire S6 (Run match algorithm + allocate) — 3 hrs
- [ ] **P3.7** Wire S7 (Wastage % analytics) — 2 hrs
- [ ] **P3.8** Wire S1 (Dashboard metrics) — 2 hrs

**Milestone M3 — App live** (target: 02 Nov)

---

## Phase 4 — Testing & Mock Data · 03 Nov – 14 Nov · ~12 hrs

**Goal:** System looks like a real busy clinic; edge cases proven.

- [ ] **P4.1** Seed script: 30 donors, 15 clinical records, 50 blood bags — 2 hrs
- [ ] **P4.2** Edge-case: register donor at 119 days → system rejects — 1 hr
- [ ] **P4.3** Edge-case: dispatch a discarded bag → hidden from match — 1 hr
- [ ] **P4.4** Edge-case: try FIFO — oldest bag dispatched first — 1 hr
- [ ] **P4.5** `docs/test_cases.md` — table of test / expected / actual — 2 hrs
- [ ] **P4.6** Bug fixing buffer — 5 hrs

**Milestone M4 — Tested** (target: 14 Nov)

---

## Phase 5 — Defense Preparation · 15 Nov – 25 Nov · ~10 hrs

**Goal:** Be able to explain and demo the system cold.

- [ ] **P5.1** Code freeze — no new features — Nov 15
- [ ] **P5.2** `docs/report.md` — architecture, 3NF, FIFO query, soft-delete rationale — 4 hrs
- [ ] **P5.3** Demo script — exact click path, no surprises — 2 hrs
- [ ] **P5.4** Mock viva — answer the 3 hard questions from memory — 2 hrs
- [ ] **P5.5** Dry run — full demo in one sitting, timed — 2 hrs

**Milestone M5 — Due** (25 Nov 2026)

---

## Continuous track (runs every week)

- **C1** Update `README.md` progress checkboxes
- **C2** Update `docs/` after each phase
- **C3** Meaningful Git commit at the end of every work session

---

## Risk Register

| Risk                                      | Impact                         | Mitigation                                                     |
| ----------------------------------------- | ------------------------------ | -------------------------------------------------------------- |
| Solo, 1 hr/day, 0 slack                   | Any missed day pushes deadline | Keep phases small; cut frontend polish before cutting database |
| Frontend wiring takes longer than planned | Compresses QA time             | Timebox each screen to 2 hrs max; ship basic if over           |
| MySQL version mismatch                    | SQL syntax errors              | Lock to MySQL 8.0 features only                                |
| Secrets leaked to GitHub                  | Security fail                  | `.env` in `.gitignore`; verify before every push               |
| Defense Q&A about AI-generated UI         | Credibility                    | Be able to explain every file, including UI wiring             |

---

## Milestone summary

- **M1** — Schema live — 03 Oct
- **M2** — API live — 18 Oct
- **M3** — App live — 02 Nov
- **M4** — Tested — 14 Nov
- **M5** — Due — 25 Nov 2026
