# VELOOP Rewards — Data Analyst Task 01 (v2, revised 20 Nov 2026)

**Analyst:** Hemavathi M · **Intern ID:** VLRINT20263720

**SIMULATED DATA — CREATED FOR ANALYTICAL TESTING.** Nothing here is actual VELOOP data or performance.

**Supplied vs generated.** Users, sessions, events, tasks, milestones and the two messy sheets are **supplied** simulated files. Rewards, Wallet, Withdrawals and Referrals were not in the shared Drive folder, so they are **analyst-generated stand-ins** (`scripts/generate_supplementary.py`, seed 20261118). Results on stand-ins are formula tests only. Replace them with real data; never mix.

## Contents
| Path | What it is |
|---|---|
| `docs/VELOOP_Task01_Final_Report.docx` (+ `.md`) | Consolidated revised report |
| `docs/VELOOP_Task01_Presentation.pptx` | 14-slide presentation with charts |
| `VELOOP_Task01_Blueprint.xlsx` | Coverage matrix, gaps, event plan, data dictionary, KPI catalogue and tests, assumptions, backlog, report facts |
| `VELOOP_Task01_Data_Profiling_and_Quality.xlsx` | Profiling, relationship tests, quality audit, cleaning log, before/after, validation, provenance, stand-in data and methodology |
| `VELOOP_Task01_Cleaned_Datasets.xlsx`, `data/cleaned/*.csv` | Cleaned (analytics-safe) users and events plus quarantine files |
| `dashboard/index.html` | Working dashboard prototype (opens in a browser; needs internet for the chart library) |
| `docs/diagrams/` | ER diagram, pipeline, 7 wireframes, charts |
| `scripts/` | All code (below) |

## Reproduce
Put the two supplied workbooks at the paths in `scripts/profile_data.py`, then run in order: `clean_data.py`, `generate_supplementary.py`, `analyze_supplementary.py`, `facts.py`, `dash_data.py`, `make_charts.py`, `make_diagrams.py`, `build_workbooks.py`, `build_report.py`. Every count in the report, workbooks and deck comes from `scripts/facts.py`.

## Known limits
Product facts are unverified (all items Proposed / To Be Verified, 15 assumptions). Support KPIs have no data. Readiness scores are analyst judgment. The dashboard was tested in a headless browser with the chart library mocked; chart drawing needs internet.
