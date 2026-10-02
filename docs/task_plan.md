# BloodLink — Solo Task Plan (final, v1.0)

**Author:** Mahmudul Hasan Mehdi (251-115-028)  
**Deadline:** 25 November 2026  
**Workload:** 1 hr/day, solo  
**Total budget:** 68 days

---

## T1 — Scope Lock, Requirements & ER Diagram

**Phase window:** 19 Sep – 27 Sep · **9 days** · **Milestone M1 — Design locked**

| ID   | Task                                               | Days | Dates          |
| ---- | -------------------------------------------------- | ---- | -------------- |
| T1.1 | Lock requirements & scope → `docs/requirements.md` | 2    | 19 – 20 Sep ✅ |
| T1.2 | Write formal proposal → `docs/proposal.md`         | 2    | 21 – 22 Sep ✅ |
| T1.3 | Write solo task plan → `docs/task_plan.md`         | 1    | 23 Sep ✅      |
| T1.4 | Draft ER diagram in Mermaid → `docs/er_diagram.md` | 2    | 26 – 27 Sep ✅ |
| T1.5 | Finalise `docs/database_design.md` (3NF writeup)   | 1    | 27 Sep ✅      |
| T1.6 | Commit phase, tag `v0.1-design`                    | 1    | 27 Sep ✅      |
| T1.7 | Allow UI-only admin login in scope docs            | 1    | 02 Oct         |

**Total:** 10 days

---

## T2 — Database Architecture

**Phase window:** 28 Sep – 03 Oct · **6 days** · **Milestone M2 — Schema live**

| ID   | Task                                                         | Days | Dates     |
| ---- | ------------------------------------------------------------ | ---- | --------- |
| T2.1 | Create `Hospitals` table                                     | 1    | 28 Sep ✅ |
| T2.2 | Create `Donors` table                                        | 1    | 02 Oct    |
| T2.3 | Create `Clinical_Records` table                              | 1    | 02 Oct    |
| T2.4 | Create `Blood_Inventory` table                               | 1    | 03 Oct    |
| T2.5 | Create `Patient_Cases` table (with directed donation)        | 1    | 03 Oct    |
| T2.6 | Create `Hospital_Requisitions` table                         | 1    | 03 Oct    |
| T2.7 | Apply foreign keys & ENUMs across all tables                 | 1    | 04 Oct    |
| T2.8 | Instantiate DB in MySQL Workbench; verify with `SHOW TABLES` | 1    | 04 Oct    |
| T2.9 | Commit phase, tag `v0.2-schema`                              | 1    | 04 Oct    |

**Total:** 9 days

---

## T3 — Flask Backend & Business Logic

**Phase window:** 05 Oct – 19 Oct · **15 days** · **Milestone M3 — API live**

| ID    | Task                                                       | Days | Dates       |
| ----- | ---------------------------------------------------------- | ---- | ----------- |
| T3.1  | Create `backend/`; virtual env; install packages           | 1    | 05 Oct      |
| T3.2  | Create `.env` + `backend/db.py` connection module          | 1    | 06 Oct      |
| T3.3  | Flask skeleton (`app.py`) + `/health` endpoint             | 1    | 07 Oct      |
| T3.4  | `/api/donors` GET — list & search                          | 1    | 08 Oct      |
| T3.5  | `/api/donors` POST — register + **120-day rule**           | 2    | 09 – 10 Oct |
| T3.6  | `/api/inventory` GET — active stock list                   | 1    | 11 Oct      |
| T3.7  | `/api/inventory` POST — new bag + **42-day expiry engine** | 1    | 12 Oct      |
| T3.8  | `/api/inventory/<id>` PATCH — **soft delete**              | 1    | 13 Oct      |
| T3.9  | `/api/requisitions` GET — pending queue                    | 1    | 14 Oct      |
| T3.10 | `/api/requisitions` POST — new hospital emergency          | 1    | 15 Oct      |
| T3.11 | `/api/match` GET — **FIFO dispatch query**                 | 2    | 16 – 17 Oct |
| T3.12 | `/api/analytics/wastage` GET — wastage %                   | 1    | 18 Oct      |
| T3.13 | Manual endpoint tests + fixes                              | 1    | 19 Oct      |
| T3.14 | Commit phase, tag `v0.3-api`                               | 1    | 19 Oct      |

**Total:** 16 days

---

## T4 — Frontend Integration

**Phase window:** 20 Oct – 03 Nov · **16 days** · **Milestone M4 — App live**

| ID    | Task                                                        | Days | Dates           |
| ----- | ----------------------------------------------------------- | ---- | --------------- |
| T4.0  | Admin login screen (UI only, AI-generated, no backend auth) | 1    | 20 Oct          |
| T4.1  | Import Google AI Studio HTML into `frontend/` (7 screens)   | 1    | 21 Oct          |
| T4.2  | Create shared `frontend/api.js` helper                      | 1    | 22 Oct          |
| T4.3  | Wire S1 (Dashboard)                                         | 2    | 23 – 24 Oct     |
| T4.4  | Wire S2 (Patient Log)                                       | 2    | 25 – 26 Oct     |
| T4.5  | Wire S3 (Donor Registry)                                    | 2    | 27 – 28 Oct     |
| T4.6  | Wire S4 (Intake Control)                                    | 2    | 29 – 30 Oct     |
| T4.7  | Wire S5 (Hub Requests)                                      | 2    | 31 Oct – 01 Nov |
| T4.8  | Wire S6 (Match & Dispatch)                                  | 2    | 02 – 03 Nov     |
| T4.9  | Wire S7 (Analytics)                                         | 1    | 03 Nov          |
| T4.10 | Commit phase, tag `v0.4-app`                                | 1    | 03 Nov          |

**Total:** 17 days

---

## T5 — Testing, Mock Data & Final Submission

**Phase window:** 04 Nov – 25 Nov · **22 days** · **Milestone M5 — Final submission**

| ID    | Task                                                        | Days | Dates       |
| ----- | ----------------------------------------------------------- | ---- | ----------- |
| T5.1  | Write `database/seed.sql` (30 donors, 15 clinical, 50 bags) | 2    | 04 – 05 Nov |
| T5.2  | Edge-case: donor at **119 days** → rejected                 | 1    | 06 Nov      |
| T5.3  | Edge-case: dispatch a **Discarded** bag → hidden            | 1    | 07 Nov      |
| T5.4  | Edge-case: **FIFO** — oldest expiry first                   | 1    | 08 Nov      |
| T5.5  | Edge-case: **directed donation** — only its patient         | 1    | 09 Nov      |
| T5.6  | Edge-case: **42-day expiry** — day 43 flagged               | 1    | 10 Nov      |
| T5.7  | Write `docs/test_cases.md`                                  | 1    | 11 Nov      |
| T5.8  | Bug fixing buffer                                           | 6    | 12 – 17 Nov |
| T5.9  | Final polish + Gantt/UIUX update                            | 2    | 18 – 19 Nov |
| T5.10 | Code freeze                                                 | 1    | 20 Nov      |
| T5.11 | Full demo dry run (timed)                                   | 1    | 21 Nov      |
| T5.12 | Extra QA buffer                                             | 3    | 22 – 24 Nov |
| T5.13 | Final commit, tag `v1.0-submission`                         | 1    | 25 Nov      |

**Total:** 22 days

---

## Continuous track (every week)

| ID   | Task                                   | When                      |
| ---- | -------------------------------------- | ------------------------- |
| TC.1 | Update `README.md` progress checkboxes | End of week               |
| TC.2 | Update `docs/` after each phase        | End of phase              |
| TC.3 | Meaningful Git commit                  | End of every work session |

---

## Milestone summary

| M   | Name             | Target Date | Tag               |
| --- | ---------------- | ----------- | ----------------- |
| M1  | Design locked    | 27 Sep      | `v0.1-design`     |
| M2  | Schema live      | 04 Oct      | `v0.2-schema`     |
| M3  | API live         | 19 Oct      | `v0.3-api`        |
| M4  | App live         | 03 Nov      | `v0.4-app`        |
| M5  | Final submission | 25 Nov      | `v1.0-submission` |

---

## Totals

| Phase                | Days                                                                |
| -------------------- | ------------------------------------------------------------------- |

| T1 — Scope & Design  | 10                                                                  |
| T2 — Database        | 9                                                                   |
| T3 — Backend         | 16                                                                  |
| T4 — Frontend        | 17                                                                  |
| T5 — Testing & Final | 22                                                                  |
| **Total**            | **74 days** across 68 calendar days (some days carry 2 short tasks) |
