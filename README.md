# COI Compliance Automation Platform

> Every rental property needs proof of insurance. This platform replaces manual PDF review with automated intake, AI validation, and tenant communication — so landlords stay compliant without drowning in paperwork.

# Woking Demo Video: 


https://github.com/user-attachments/assets/1dfbc50e-dda7-4a57-a25b-4f33cc92a38b





## COI Compliance Automation Platform User Guide:

https://app.trupeer.ai/view/omcZ7gVJN/coi-compliance-automation-platform-user-guide

## Live Link: https://complinace-hub.framer.ai/

---

## Table of Contents

- [Why This Product Exists](#why-this-product-exists)
- [The Problem in Detail](#the-problem-in-detail)
- [Who This Is For](#who-this-is-for)
- [The Solution](#the-solution)
- [How It Works](#how-it-works)
- [Core Features](#core-features)
- [Multi-Agent AI Pipeline](#multi-agent-ai-pipeline)
- [Email Automation](#email-automation)
- [COI Versioning](#coi-versioning)
- [Checklist Engine](#checklist-engine)
- [Editable Email Templates](#editable-email-templates)
- [Metrics & ROI](#metrics--roi)
- [Technology Stack](#technology-stack)
- [Architecture Overview](#architecture-overview)
- [Phased Roadmap](#phased-roadmap)
- [Success Criteria](#success-criteria)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)

---

## Why This Product Exists

When a landlord rents out a condo in Florida, a retail unit in Toronto, or an apartment building in Vancouver, the lease almost always requires one thing before keys are handed over: a **Certificate of Insurance (COI)**.

A COI is not the insurance policy itself. It is a one-page summary that proves the tenant (or their business) carries active liability coverage — and that the landlord is protected if something goes wrong on the property.

**That single document creates a recurring compliance burden that grows with every unit you own.**

| Portfolio size | COIs to manage per year | Manual effort (at ~20 min each) |
|----------------|-------------------------|----------------------------------|
| 10 units | ~20 (move-in + renewal) | ~7 hours |
| 50 units | ~100 | ~33 hours |
| 200 units | ~400 | ~133 hours (~17 working days) |

Most landlords and property managers still handle this the same way they did ten years ago: **email inboxes, PDF attachments, and a human opening every file by hand.** That process breaks the moment you scale beyond a handful of tenants.

**This product exists because COI compliance is mandatory, repetitive, high-risk, and completely unsuited to manual work at scale.**

---

## The Problem in Detail

### What landlords are legally and contractually required to verify

Before accepting a tenant — and again at every policy renewal — the landlord must confirm:

| Requirement | What can go wrong if missed |
|-------------|---------------------------|
| **Liability limits** | Coverage below lease minimum ($1M USD / $2M CAD) — landlord exposed in a claim |
| **Additional insured** | Landlord not named on the policy — no protection during incidents |
| **Policy dates** | Gap between expiry and renewal — property operates uninsured |
| **Required endorsements** | Missing waiver of subrogation or primary/non-contributory clause — lease violation |
| **Certificate holder** | Wrong name or address — document may not be legally binding |
| **Carrier validity** | Unknown or non-admitted insurer — coverage may not pay out |

Each COI is a PDF with different formatting from different insurers. No two look the same. A property manager must read every line, cross-check against the lease, and decide: accept or reject.

### What the current process looks like

```
Tenant emails COI PDF
        ↓
Email sits in shared inbox (hours or days)
        ↓
Property manager opens PDF manually
        ↓
Compares against checklist (spreadsheet / memory / lease binder)
        ↓
Maybe accepts, maybe sends vague "please fix" email
        ↓
Tenant resubmits — often the same mistake
        ↓
No one tracks when the policy expires
        ↓
Coverage lapses silently
        ↓
Incident happens — landlord discovers tenant was uninsured
```

This cycle repeats for **every tenant, every year, every property**.

### Where the current approach fails

| Failure | What happens | Real-world impact |
|---------|--------------|-------------------|
| **No central tracking** | COIs scattered across email threads | Documents lost; compliance status unknown |
| **Inconsistent review** | Different staff apply different standards | Some tenants slip through with deficient coverage |
| **Slow turnaround** | 15–30 minutes per COI, done when someone has time | Move-ins delayed; tenants frustrated |
| **Vague rejections** | "Your COI is not acceptable" with no specifics | Tenants resubmit wrong documents; cycle repeats |
| **No version history** | Re-submissions treated as new emails | No record of what was wrong or what changed |
| **No expiry monitoring** | Nobody tracks renewal dates proactively | Properties operate with lapsed coverage |
| **No audit trail** | Decisions made in email, not logged | Disputes, lender audits, and legal claims become unwinnable |

### The cost is not just time — it is uncovered liability

**In the USA (e.g. Florida, Texas):**
- Slip-and-fall or property damage claim hits an uninsured tenant → landlord's own policy may not cover it
- Lenders and HOAs require proof of tenant insurance — non-compliance blocks refinancing or sale
- Lease default grounds if tenant fails to maintain required coverage
- Florida condo associations and property managers often require COIs before tenant move-in

**In Canada (e.g. Ontario, British Columbia):**
- Commercial and residential leases require tenants to carry liability insurance and name the landlord as additional insured
- Condo corporations and property management firms mandate COIs for vendors, contractors, and commercial tenants
- Provincial tenancy and commercial lease standards tie insurance proof to ongoing compliance
- Uninsured contractor or tenant incident → landlord bears the financial and legal burden

> **One missed clause on one tenant's COI can cost more than a year of property management fees.**

Spreadsheets, shared inboxes, and manual PDF review do not fail because people are careless. They fail because **the process was never designed to scale**.

---

## Who This Is For

- **Individual landlords** managing 5–50+ rental units across one or more properties
- **Property managers** handling COI compliance for multiple owners
- **Small portfolio operators** who need one place to see what is compliant, what is expiring, and what was rejected

At launch, a **single admin login** runs the entire platform — upload, review, approve, and configure. No complex role hierarchy until the product matures.

---

## The Solution

### One platform. Full COI lifecycle. Minimal manual work.

This product replaces the broken email-and-spreadsheet workflow with a **single automated pipeline** — from the moment a tenant sends a COI to the moment compliance is tracked on a live dashboard.

```
BEFORE (today)                          AFTER (this platform)
─────────────────                       ─────────────────────
Email inbox full of PDFs        →       Dedicated intake (email + dashboard)
Someone opens each PDF by hand  →       AI reads, extracts, and validates
Checklist in someone's head     →       Editable checklist enforced on every doc
Vague rejection emails            →       Specific deficiency emails (editable templates)
Re-submissions get lost           →       Version history per tenant (v1, v2, v3…)
Nobody tracks expiry              →       node-cron schedules reminders at 30 / 14 / 7 / 3 days (BullMQ sends email)
No compliance visibility          →       Live dashboard with metrics and audit trail
```

### How each problem maps to a product capability

| Problem today | How this product solves it |
|---------------|---------------------------|
| COIs lost in email threads | Dedicated inbox (`maniranjan@agentmail.to`) + dashboard — every document stored in Cloudinary with a database record |
| Manual PDF review takes 15–30 min each | Multi-agent AI pipeline reads the document, extracts fields, and compares against your checklist in minutes |
| Inconsistent review standards | Same editable checklist applied to every COI — no human variance in what gets checked |
| Vague rejection emails | Editable email templates with exact missing items, rejection reasons, and policy details |
| Re-submissions treated as new cases | COI versioning per sender — v1 rejected, v2 re-uploaded, full history and comparison |
| No expiry tracking | AI extracts expiry date; **node-cron** detects due reminders at 30/14/7/3 days; **BullMQ worker** sends emails; expired COIs flagged non-compliant |
| No audit trail | Every upload, AI step, email, and admin decision logged with timestamps |
| No portfolio visibility | Metrics dashboard — compliance %, expiring soon, ROI, turnaround time |

### The end-to-end flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        INTAKE                                    │
│  Tenant emails COI  ──┐                                         │
│  Admin uploads COI  ──┼──►  Store in Cloudinary  ──►  Queue job │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   AI REVIEW (automated)                          │
│  Classify document → OCR if needed → Extract fields →           │
│  Compare checklist → Flag risks → Generate recommendation       │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   HUMAN REVIEW (2 min, not 20)                     │
│  Admin sees AI summary + risks + recommendation →               │
│  Accept or Reject with reason                                   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   TENANT COMMUNICATION (automated)               │
│  Approved → acceptance email                                    │
│  Rejected → deficiency email with exact missing items            │
│  Missing attachment → request email                             │
│  Expiring soon → renewal reminder with policy details           │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   COMPLIANCE TRACKING (always on)                │
│  Dashboard status · Expiry monitoring · Metrics · Audit log     │
└─────────────────────────────────────────────────────────────────┘
```

### The core principle

**You define the compliance rules once — in the checklist and email templates. The system enforces them on every document, forever.**

- AI does the reading and comparison
- Admin does the final decision (accept / reject)
- Tenants get clear, specific communication automatically
- Nothing expires without a reminder
- Every action is logged

**Result:** Review time drops from ~20 minutes to ~2 minutes per COI. Compliance becomes visible, consistent, and auditable — not a guessing game in a shared inbox.

---

## How It Works

### Intake (two channels, one pipeline)

1. **Email** — Tenants forward COIs to `maniranjan@agentmail.to`. AgentMail webhook delivers body + attachments to the backend.
2. **Dashboard** — Admin uploads COIs directly from the web UI.

Both paths create a database record, upload the file to **Cloudinary**, and enqueue a **BullMQ** job. Same processing. Same standards. No channel bias.

### Processing (multi-agent AI — Phase 4)

**Pre-pipeline:** Validate COI PDF exists (before OCR). **LlamaParse** extracts text from PDF + email body.

A chain of five specialized agents runs **sequentially** (Groq models via **OpenAI SDK** + **OpenAI Agents SDK** guardrails). Each agent is a separate run with its own **input guardrail** (before) and **output guardrail** (after):

1. **Document Agent** — Is this a valid COI? Early exit if not.
2. **Extraction Agent** — Structured JSON: carrier, limits, dates, insured, policy #, endorsements.
3. **Checklist Agent** — Compare against DB checklist; status per item: **PASS / FAIL / MISSING** (never UNKNOWN).
4. **Risk & Gap Agent** — Mandatory failures, risk level, low-confidence fields (runs even when clauses are missing).
5. **Report Agent** — Draft summary, citations, recommendation, suggested email text for admin review.

**Reliability:** Zod JSON validation after every agent · Groq model **fallback chain** on 429/503/unavailable only · **Logfire** tracing per job.

### Human-in-the-loop

AI **recommends**. Admin **decides**.

Agent 5 produces an **editable draft report** (Phase 5 UI). Admin reviews, edits if needed, then sends email via AgentMail. Accept or reject with a reason. Tenant receives a **template-based email** (not the raw internal agent dump).

### Versioning

Tenant uploads → rejected → uploads again?

That's **Version 2** (not a new case). Full history per sender. Compare what changed. Never lose the original.

### Renewal

AI extracts expiry date. **node-cron** runs daily, finds COIs due for reminders at **30, 14, 7, and 3 days** before expiry, and enqueues **BullMQ** `send-reminder` jobs. The worker delivers emails via AgentMail (with retries). Expired COIs flagged **non-compliant** until a new version is accepted.

---

## Core Features

### 1. Admin Login (Simple)

- Single admin account with full platform access
- No multi-role system at launch (Executive, Department Head, Auditor deferred)
- JWT-based session authentication

### 2. COI Dashboard

- Upload COIs manually from the web UI
- Receive COIs via forwarded email
- Search, filter, and sort all submissions
- Status tracking:
  - **Pending Review** — AI done or in progress, awaiting admin
  - **Accepted** — Admin approved
  - **Rejected** — Admin rejected with reason
  - **Expiring Soon** — Within 30-day renewal window
  - **Expired** — Past expiry date, non-compliant
- View documents inline (served from Cloudinary)
- View AI review results (risks, missing items, summary, recommendation)
- Internal notes per COI
- Event timeline (upload → AI → decision → emails → reminders)
- Export compliance data

### 3. Cloudinary Document Storage

- Every COI version stored in Cloudinary
- Original file never overwritten
- Secure URL + metadata stored in Neon PostgreSQL
- Supports PDF and common document formats

### 4. COI Versioning (Per Sender)

- Each tenant/sender has one COI case with multiple versions
- **Version 1** uploaded → rejected → **Version 2** re-uploaded → tracked independently
- Side-by-side version comparison (what changed between uploads)
- Latest version = current active submission
- Older versions preserved in full history
- Timeline per version: upload → AI review → decision → re-upload

### 5. Editable Checklist Engine

- Dedicated **Checklist** section in admin
- View all checklist requirements
- **Add** new requirements
- **Edit** existing requirements (name, expected value, mandatory flag, category)
- **Delete / disable** requirements
- Optional import from PDF, DOCX, or CSV as a starting point
- Checklist is the source of truth for every AI review

Each checklist item contains:

| Field | Description |
|-------|-------------|
| Requirement | Name of the clause or field to verify |
| Expected Value | What the value should be (e.g. "$1M", "Landlord name") |
| Mandatory | Whether failure blocks acceptance |
| Category | Grouping (e.g. Liability, Dates, Endorsements) |

### 6. BullMQ Job Processing

BullMQ is the **async worker layer** backed by **Redis**. See [Queue & Reliability Specification](#queue--reliability-specification) for queue names, retries, and DLQ rules.

| Job type | Queue | Triggered by | What it does |
|----------|-------|--------------|--------------|
| `process-coi` | `coi-jobs` | Dashboard upload or AgentMail webhook | Cloudinary → AI agent chain (Phase 4) → update status |
| `send-template-email` | `coi-jobs` | Admin accept/reject, intake events (Phase 5) | Send templated outbound email via AgentMail |
| `send-reminder` | `reminder-jobs` | **node-cron** daily expiry scan (Phase 6) | Send renewal reminder email via AgentMail |

**Job statuses (stored in Neon `CoiJob`):**
- **Queued** — Waiting in Redis to be picked up
- **Processing** — Worker is running
- **Ready for Review** — AI complete (Phase 4+), awaiting admin
- **Failed** — Retrying with exponential backoff
- **DLQ** — Max retries exceeded; in dead-letter queue for human inspection

**Reliability (all main queues):**
- Exponential backoff retries (default: 5 attempts, 5s base delay)
- Failed jobs routed to matching DLQ after final attempt
- Real-time status visible on dashboard (Phase 2+)

**Email jobs (`send-reminder`, `send-template-email`):**
- Picked up by BullMQ worker(s) — same process can listen to both `coi-jobs` and `reminder-jobs`
- Retries on AgentMail delivery failure; DLQ on exhaustion
- Logged in audit trail (template, recipient, timestamp)

### 7. AgentMail Email Intake

- Monitors `maniranjan@agentmail.to`
- Webhook receives email body + attachments on `message.received`
- Missing attachment → immediate templated reply
- Valid attachment → acknowledge receipt, upload to Cloudinary, enqueue BullMQ job
- All emails linked to COI record and version on dashboard
- Outbound replies sent via AgentMail API

### 8. Multi-Agent AI Review (Phase 4)

- Sequential specialist agents with **input/output guardrails** on every step
- **LlamaParse** OCR for PDF + email body (not Groq OCR)
- Document classification — early exit if not a COI
- Structured field extraction (carrier, limits, dates, policy #, named insured)
- Checklist comparison with per-item **PASS / FAIL / MISSING**
- Risk detection and mandatory failure analysis (Agents 4 & 5 run even when clauses are missing)
- Zod JSON validation + Groq model fallback on rate limits
- **Logfire** tracing per job; `AiRun` + `AgentStep` stored in Neon
- Draft report with citations and suggested email text for admin (Phase 5 edit + send)

### 9. Admin Review & Decision (Phase 5)

- Review full AI output per COI version
- **Edit** Agent 5 draft report (summary, missing items, citations) before sending
- **Accept** or **Reject** with mandatory rejection reason
- **Send email** — output guardrail on final text → template → AgentMail
- Decision applies to that specific version
- If rejected, sender can submit a new version (creates next version number)
- All decisions logged permanently in audit trail
- Hybrid email: auto for missing attachment / unreadable file; admin approval for AI outcomes

### 10. Editable Email Templates

Admin-editable templates with defined placeholders for every scenario. Preview with sample data before saving.

| Template | When Sent |
|----------|-----------|
| **Missing Attachment** | Email received with no COI file attached |
| **Receipt Acknowledged** | Valid attachment received, processing started |
| **Clauses / Items Missing** | Checklist failed — lists exactly what's missing or not found |
| **All Matched — Awaiting Review** | Checklist passed — waiting for admin decision |
| **Approved** | Admin accepted — includes matched checklist summary |
| **Rejected** | Admin rejected — includes rejection reason + deficient items |
| **Renewal Reminder** | 30 / 14 / 7 / 3 days before expiry — policy details + resubmit instructions (node-cron enqueues → BullMQ worker sends) |
| **Processing Error** | Job failed — notify sender of delay |

**Available placeholders:**

| Placeholder | Description |
|-------------|-------------|
| `{{sender_name}}` | Tenant/sender display name |
| `{{sender_email}}` | Tenant email address |
| `{{property_name}}` | Property or unit identifier |
| `{{expiry_date}}` | Policy expiration date |
| `{{policy_number}}` | Insurance policy number |
| `{{carrier_name}}` | Insurance carrier name |
| `{{missing_items}}` | List of failed/missing checklist items |
| `{{rejection_reason}}` | Admin's rejection reason |
| `{{version_number}}` | Current COI version (v1, v2, etc.) |
| `{{submission_date}}` | Date COI was received |
| `{{matched_items}}` | List of passed checklist items |
| `{{ai_summary}}` | AI-generated document summary |

### 11. Expiry & Renewal Engine

- Expiry date extracted by AI from each accepted COI
- **node-cron** runs a daily scheduled task that scans the database for COIs expiring in **30, 14, 7, or 3 days**
- For each match, cron **enqueues `send-reminder` on `reminder-jobs`** (does not send email directly; never uses `coi-jobs`)
- **BullMQ worker** picks up from `reminder-jobs`, renders **Renewal Reminder** template, sends via AgentMail
- On max retries → `reminder-jobs-dlq` for human inspection
- **ReminderLog** table prevents duplicate reminders for the same COI + day-offset
- Expired COIs marked **non-compliant**
- Non-compliant until new version uploaded and accepted by admin

> **Note:** **node-cron** decides *who* needs a reminder and enqueues to **`reminder-jobs`**; **BullMQ worker** sends the email. Cron never calls AgentMail directly.

### 12. Metrics Dashboard

| Widget | Description |
|--------|-------------|
| Portfolio Compliance % | % of active COIs that are accepted |
| Total COIs | All COIs ever received |
| Active COIs | Accepted and not yet expired |
| Rejected COIs | Count of rejected submissions |
| Expiring Soon | COIs within 30-day window |
| ROI | Return on platform investment |
| Cost Savings | Dollar value of hours saved |
| Capacity Created | Total hours freed from manual review |
| Agent Response Time | AI processing speed |
| Compliance Resolution Time | End-to-end cycle time |
| Workload Automation % | % of reviews handled without manual PDF reading |

### 13. Audit & Compliance History

- Immutable original documents in Cloudinary (never overwritten)
- Full audit log:
  - Document uploads (dashboard + email)
  - BullMQ job lifecycle
  - Each AI agent step and output
  - Emails sent (template used, recipient, timestamp)
  - Admin decisions (accept/reject + reason)
  - Checklist changes
  - Email template edits
- Complete timeline per COI and per sender

---

## Multi-Agent AI Pipeline

```
┌─────────────────┐
│  Intake check   │  COI PDF attached? (webhook / worker pre-check)
└────────┬────────┘
         │ no PDF → auto email: Missing Attachment (no agents)
         ▼
┌─────────────────┐
│  LlamaParse     │  OCR/text from PDF + email body
└────────┬────────┘
         │ unreadable → auto email: Processing Error (no agents)
         ▼
┌─────────────────┐
│  Agent 1        │  Document classification
│  + guardrails   │  → Is it a COI?
└────────┬────────┘
         │ not COI → draft for admin → Send email (Phase 5)
         ▼
┌─────────────────┐
│  Agent 2        │  Structured field extraction + guardrails
│  Extraction     │  → Carrier, limits, dates, insured, policy #
└────────┬────────┘
         ▼
┌─────────────────┐
│  Agent 3        │  Checklist comparison + guardrails
│  Checklist      │  → PASS / FAIL / MISSING per DB checklist item
└────────┬────────┘
         ▼
┌─────────────────┐
│  Agent 4        │  Risk & gap analysis + guardrails
│  Risk & Gaps    │  → Mandatory failures, risk level, confidence
└────────┬────────┘
         ▼
┌─────────────────┐
│  Agent 5        │  Draft report + guardrails
│  Report         │  → Summary, citations, suggested email text
└────────┬────────┘
         ▼
┌─────────────────┐
│  Admin Review   │  Edit draft → Send / Accept / Reject (Phase 5)
└─────────────────┘
```

### Agent Details

| Agent | Input | Output | Early Exit |
|-------|-------|--------|------------|
| **Pre-check** | Webhook / upload | PDF present or not | No PDF → no agents, auto Missing Attachment email |
| **LlamaParse** | Cloudinary PDF + email body | Markdown/text bundle | Unreadable → auto Processing Error email |
| **Document** | OCR text | `isCoi`, clean text, document type | Not COI → skip agents 2–5, admin sends email |
| **Extraction** | Clean text | Structured JSON: carrier, limits, dates, policy #, insured | — |
| **Checklist** | Extraction + DB checklist | Per-item **PASS / FAIL / MISSING** | — |
| **Risk & Gaps** | Checklist + extraction | Risk flags, mandatory failures, confidence | Always runs if Agent 3 ran |
| **Report** | All prior outputs | Draft summary, citations, recommendation, suggested template | Always runs if Agent 3 ran |

Each agent's input/output and guardrail results are stored in **`AiRun`** + **`AgentStep`** — full transparency and auditability.

### Guardrails (OpenAI Agents SDK)

Per [OpenAI guardrails guide](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals): **input guardrails** before each agent (`runInParallel: false`), **output guardrails** before passing to the next agent. Tripwire → stop pipeline, log reason in Logfire, admin sends safe email (Phase 5).

| Agent | Input guardrail | Output guardrail |
|-------|-----------------|------------------|
| 1 Document | Injection, jailbreak, harmful content in OCR text | Valid classification JSON |
| 2 Extraction | Safe prior output | Zod-valid extraction JSON |
| 3 Checklist | Grounding: extraction + DB checklist only | All items evaluated; no UNKNOWN |
| 4 Risk | Complete checklist + extraction inputs | No hallucinated risk flags |
| 5 Report | All prior outputs present | Report matches checklist; no invented missing clauses |

### Hybrid email rules (Phase 4 auto · Phase 5 admin)

| Scenario | Agents | Email timing |
|----------|--------|--------------|
| No COI PDF | None | **Auto** → Missing Attachment |
| Unreadable file | None | **Auto** → Processing Error |
| Valid PDF received | — | **Auto** → Receipt Acknowledged (optional) |
| Not a COI | Agent 1 only | **Admin Send** after review |
| Guardrail tripwire | Stops mid-pipeline | **Admin Send** (safe generic message) |
| Checklist MISSING/FAIL | Full 1–5 | **Admin Send** after edit → Clauses / Items Missing |
| All checklist PASS | Full 1–5 | **Admin Accept/Send** → All Matched / Approved |

**AI stack:** Groq LLM via OpenAI SDK · **LlamaParse** for OCR · **Logfire** for observability · Groq-only model fallback (not task-based routing).

---

## Email Automation

Tenants never need to log in. They email COIs. The system handles the rest.

```
Tenant emails COI to maniranjan@agentmail.to
      │
      ├─ No attachment?     → "Please resend with your COI attached"
      ├─ Attachment received → "Received, we're reviewing your COI"
      ├─ Checklist failed   → "Missing: [detailed list of deficiencies]"
      ├─ Checklist passed   → "Under review, we'll confirm shortly"
      ├─ Admin approved     → "Your COI has been accepted"
      ├─ Admin rejected     → "Rejected: [reason + what to fix]"
      ├─ Expiry approaching → "Your COI expires on [date], please renew"
      └─ Processing error   → "We're experiencing a delay, hang tight"
```

All templates are **editable by admin** with live placeholder preview.

---

## COI Versioning

### Example lifecycle for one tenant

```
Sender: john@tenant.com
Property: Unit 4B, Oak Street Apartments

Version 1 (Jan 5)
  ├── Uploaded via email
  ├── AI: Missing additional insured clause
  ├── Admin: REJECTED — "Landlord not listed as additional insured"
  └── Email: Rejection template sent with missing items

Version 2 (Jan 12)
  ├── Re-uploaded via email
  ├── AI: All checklist items pass
  ├── Admin: ACCEPTED
  └── Email: Approval template sent

Version 3 (Dec 1 — renewal)
  ├── Uploaded before expiry
  ├── AI: Processing...
  └── Status: Pending Review
```

- All versions visible in dashboard under one sender record
- Compare v1 vs v2 to see what the tenant fixed
- Only the latest accepted version counts as compliant
- Expired versions do not count toward compliance %

---

## Checklist Engine

### Default checklist categories

| Category | Example Requirements |
|----------|---------------------|
| **General Liability** | Minimum limit ($1M / $2M), occurrence vs aggregate |
| **Additional Insured** | Landlord named as additional insured |
| **Policy Dates** | Effective date, expiration date, covers lease term |
| **Endorsements** | Waiver of subrogation, primary & non-contributory |
| **Carrier** | AM Best rating, admitted carrier |
| **Certificate Holder** | Correct landlord name and address |

### How matching works

1. AI extracts values from the COI document
2. Each checklist requirement is compared against the extracted value
3. Result per item: **Pass**, **Fail**, or **Not Found**
4. Mandatory failures block acceptance
5. All results stored and shown to admin with citations

---

## Editable Email Templates

Templates are stored in the database and editable from the admin settings page.

### Template editor features

- Rich text or plain text editing
- Placeholder picker (insert `{{placeholder}}` with one click)
- Live preview with sample data
- Version history of template changes (audit log)

### Example: Rejection template

```
Hi {{sender_name}},

Thank you for submitting your Certificate of Insurance for {{property_name}}.

After review, we were unable to accept your COI (Version {{version_number}}) for the following reasons:

{{rejection_reason}}

Missing or deficient items:
{{missing_items}}

Please correct these issues and resubmit your updated COI by replying to this email with the corrected document attached.

Best regards,
Property Management
```

---

## Metrics & ROI

### Calculations

| Metric | Formula | Why It Matters |
|--------|---------|----------------|
| **Compliance %** | `(Accepted Active COIs ÷ Total Active COIs) × 100` | Portfolio health at a glance |
| **ROI** | `(Total Savings ÷ Platform Cost) × 100` | Justify the platform to stakeholders |
| **Cost Savings** | `Hours Saved × Hourly Rate` | Quantify manual work eliminated |
| **Capacity Created** | `Total Hours Saved` | PM time freed for higher-value work |
| **Working Days Saved** | `Hours Saved ÷ 8` | Executive-friendly reporting |
| **Agent Response Time** | `AI Completion Time − Email Received Time` | Tenant experience SLA |
| **Compliance Resolution Time** | `Final Acceptance Date − First Submission Date` | End-to-end cycle time |
| **Workload Automation %** | `(COIs reviewed by AI only ÷ Total COIs) × 100` | How much manual PDF reading was eliminated |

### Definitions

- **Active COI** = Accepted and not yet expired
- **Expiring Soon** = Expiry within the 30-day reminder window
- **Expired** = Past expiry date; treated as non-compliant until replaced and accepted

### Example ROI

```
200 tenants × 20 min manual review = 66+ hours per renewal cycle
At $50/hr = $3,300 saved per cycle
× 2 renewal cycles/year = $6,600/year in labor savings
Before counting risk reduction from missed expiries
```

---

## Technology Stack

| Layer | Technology | Role |
|-------|-----------|------|
| **Full-stack app** | Next.js 15 (App Router), TypeScript, Tailwind CSS, shadcn/ui | **Frontend:** dashboard, COI viewer, checklist, templates, metrics · **Backend:** API routes, webhooks, auth, business logic |
| **Database** | Neon PostgreSQL | COI records, versions, checklist, templates, audit logs, metrics |
| **ORM** | Prisma or Drizzle | Schema management, migrations, type-safe queries |
| **File Storage** | Cloudinary | Immutable COI originals, secure URLs, PDF delivery |
| **Job Queue** | BullMQ + Redis | Four queues: `coi-jobs`, `coi-jobs-dlq`, `reminder-jobs`, `reminder-jobs-dlq` |
| **Scheduler** | node-cron (daily) | Scans expiry dates → enqueues to `reminder-jobs` only (never sends email directly) |
| **AI** | OpenAI SDK + OpenAI Agents SDK → Groq LLM; LlamaParse OCR; Logfire tracing | Multi-agent pipeline with guardrails |
| **Email** | AgentMail (`maniranjan@agentmail.to`) | Inbound COI intake + outbound templated replies |
| **Auth** | JWT (via Next.js API routes) | Single admin session |

---

## Queue & Reliability Specification

Implementation reference for Phases 2–6. **Redis** stores jobs; **BullMQ** manages queues, workers, retries, and DLQ routing.

### Queue layout (4 queues)

| Queue | Purpose | Job types |
|-------|---------|-----------|
| **`coi-jobs`** | COI intake, AI processing, templated emails | `process-coi`, `send-template-email` |
| **`coi-jobs-dlq`** | Failed COI jobs after max retries | Human inspection + manual retry |
| **`reminder-jobs`** | Renewal reminder emails only | `send-reminder` |
| **`reminder-jobs-dlq`** | Failed reminder jobs after max retries | Human inspection + manual retry |

**Why separate reminder queue?** Isolates daily reminder traffic from heavy COI/AI work; independent monitoring and scaling.

```
Dashboard / Webhook  ──►  coi-jobs  ──►  worker
                               │ fail (max retries)
                               ▼
                         coi-jobs-dlq

node-cron (daily)    ──►  reminder-jobs  ──►  worker
                               │ fail (max retries)
                               ▼
                         reminder-jobs-dlq
```

### Retry policy (exponential backoff)

Applied to all jobs enqueued on `coi-jobs` and `reminder-jobs`:

```ts
{
  attempts: 5,
  backoff: { type: 'exponential', delay: 5000 },  // 5s → 10s → 20s → 40s → 80s
  removeOnComplete: 100,
  removeOnFail: false,
}
```

Configurable via environment variables (see [Environment Variables](#environment-variables)).

### Dead Letter Queue (DLQ) flow

1. Job fails in worker → BullMQ retries with exponential backoff
2. After **final attempt** → move to matching DLQ (`coi-jobs-dlq` or `reminder-jobs-dlq`)
3. Update Neon `CoiJob` status → `DLQ`, store `failureReason` and `dlqJobId`
4. Dashboard shows failed/DLQ jobs for admin inspection
5. Admin can **retry from DLQ** (re-enqueue to main queue) — Phase 2+

### Idempotency

| Scenario | Mechanism |
|----------|-----------|
| AgentMail webhook duplicate | Dedup by `messageId` in Redis or DB before enqueue |
| Reminder duplicate | `ReminderLog` in Postgres (`coiId` + `daysBefore` unique) |
| Cron runs twice | Redis distributed lock with token + TTL renewal during daily scan (Phase 6) |
| DLQ triage | `/dashboard/jobs` — filter COI vs reminder, retry or dismiss (Phase 6) |

### npm packages (Phase 2+)

```bash
npm install bullmq ioredis agentmail
npm install node-cron    # Phase 6
```

### Processes to run

| Process | Command | Phase |
|---------|---------|-------|
| Next.js app | `npm run dev` | 1+ |
| BullMQ worker | `npm run worker` | 2+ |
| node-cron scheduler | `npm run cron` | 6 |
| Ops smoke test | `npm run test:ops` | 6 |

**Jobs dashboard** (`/dashboard/jobs`): live queue depth, cron scan history, DLQ filters (All/COI/Reminders), retry and dismiss actions.

**Health probes** (no auth): `GET /api/health`, `/api/health/database`, `/api/health/redis`, `/api/health/queue`.

---

## Architecture Overview

![COI Platform System Architecture](docs/diagram-export-7-7-2026-12_56_40-PM.png)

*Full system architecture — intake (AgentMail + dashboard), Next.js app, Neon/Cloudinary/Redis, BullMQ worker, 5-agent AI pipeline (Groq + LlamaParse), admin review loop, and outbound email.*

<details>
<summary>ASCII diagram (legacy reference)</summary>

```
                    ┌──────────────────────────────────────────────┐
                    │              Next.js (full-stack)             │
                    │  ┌────────────────┐  ┌─────────────────────┐  │
                    │  │    Frontend    │  │   Backend (API)     │  │
                    │  │  Dashboard ·   │  │  Route handlers ·   │  │
                    │  │  Checklist ·   │  │  Webhooks · Auth ·  │  │
                    │  │  Templates ·   │  │  COI CRUD · Upload  │  │
                    │  │  Metrics       │  │                     │  │
                    │  └────────────────┘  └──────────┬──────────┘  │
                    └─────────────────────────────────┼────────────┘
                                                        │
              ┌──────────────┬──────────────┬───────────┘
              │              │              │
     ┌────────▼───┐  ┌───────▼──────┐  ┌───▼────────────────────────┐
     │ Neon PG    │  │  Cloudinary  │  │   Redis / BullMQ           │
     │ (records)  │  │  (documents) │  │   coi-jobs · coi-jobs-dlq    │
     └────────────┘  └──────────────┘  │   reminder-jobs · reminder-dlq│
                                         └───┬────────────────────────┘
                                            │
                    ┌───────────────────────▼──────────┐
                    │  BullMQ Worker (same repo)       │
                    │  coi-jobs: process-coi ·         │
                    │            send-template-email   │
                    │  reminder-jobs: send-reminder    │
                    └───────────────────────┬──────────┘
                                            │
                    ┌───────────────────────▼──────────┐
                    │  AgentMail (inbound + outbound)  │
                    │  maniranjan@agentmail.to         │
                    └──────────────────────────────────┘

                    ┌──────────────────────────────────┐
                    │  node-cron (daily, Phase 6)      │
                    │  Scan expiry → enqueue to        │
                    │  reminder-jobs (not coi-jobs)    │
                    └──────────────────────────────────┘
```

</details>

### Design Principles

- **Cron schedules, BullMQ executes** — node-cron enqueues to `reminder-jobs`; worker sends via AgentMail
- **Queue isolation** — COI processing (`coi-jobs`) separate from reminders (`reminder-jobs`)
- **Exponential backoff + DLQ** — failed jobs retry automatically; exhausted jobs go to DLQ for human inspection
- **Single intake pipeline** — email and dashboard upload converge at `coi-jobs` `process-coi`; no duplicate logic
- **Immutable documents** — Cloudinary stores originals; new versions are new uploads, not overwrites
- **Human-in-the-loop** — AI recommends; admin decides; tenants are never auto-accepted without review
- **Audit everything** — every agent step, email, and decision is logged with timestamp
- **Sequential agents** — each agent has one job; output feeds the next; early exit on invalid documents
- **Editable config** — checklist and email templates managed by admin without code changes

### Data Flow

```
1. INTAKE
   Email (AgentMail webhook) ──┐
                               ├──► Create COI record in Neon
   Dashboard upload ───────────┘    Upload file to Cloudinary
                                    Enqueue coi-jobs (process-coi)

2. PROCESSING (BullMQ Worker — coi-jobs)
   Job picked up ──► Agent 1 (Document/OCR)
                 ──► Agent 2 (Extraction)
                 ──► Agent 3 (Checklist)
                 ──► Agent 4 (Risk/Gaps)
                 ──► Agent 5 (Report)
                 ──► Save all outputs to Neon
                 ──► Update status: Ready for Review
                 ──► Enqueue coi-jobs (send-template-email)

3. ADMIN REVIEW
   Admin views AI results ──► Accept or Reject with reason
                          ──► Enqueue coi-jobs (send-template-email: Approved / Rejected)
                          ──► Update COI status
                          ──► Log decision in audit trail

4. RENEWAL (node-cron + BullMQ — Phase 6)
   Daily node-cron ──► Scan DB for COIs expiring in 30 / 14 / 7 / 3 days
                   ──► Enqueue reminder-jobs (send-reminder) per match
   BullMQ worker  ──► Send Renewal Reminder via AgentMail (exponential backoff)
                   ──► On max retries → reminder-jobs-dlq
                   ──► Log in ReminderLog (idempotent — no duplicate sends)
                   ──► Mark expired COIs as non-compliant
                   ──► Update metrics dashboard
```

---

## Implementation Reference

Spec for building each phase. Runbooks: `docs/PHASE1.md`, `docs/PHASE2.md`, etc.

### Database schema by phase

**Phase 1 (implemented)** — `CoiDocument`

**Phase 2** — add `CoiJob`:

```prisma
enum JobStatus {
  QUEUED
  PROCESSING
  READY_FOR_REVIEW
  FAILED
  DLQ
}

enum JobType {
  PROCESS_COI
  SEND_TEMPLATE_EMAIL
  SEND_REMINDER
}

model CoiJob {
  id            String    @id @default(cuid())
  coiDocumentId String
  coiDocument   CoiDocument @relation(fields: [coiDocumentId], references: [id])
  bullmqJobId   String?
  queueName     String    // coi-jobs | reminder-jobs
  type          JobType
  status        JobStatus @default(QUEUED)
  attempts      Int       @default(0)
  failureReason String?
  dlqJobId      String?
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
}
```

**Phase 3** — `Sender`, `CoiVersion` (link `CoiJob` → version)

**Phase 4** — `AiRun`, `AgentStep`, extracted fields JSON, draft report + citations on `CoiVersion`

**Phase 5** — `EmailTemplate`, `OutboundEmail`

**Phase 6** — `ReminderLog` (`coiDocumentId`, `daysBefore`, `sentAt` — unique per pair)

### API routes by phase

| Route | Phase | Purpose |
|-------|-------|---------|
| `POST /api/auth/login` | 1 | Admin sign-in |
| `GET/POST /api/coi` | 1–2 | List / upload (Phase 2: enqueue `coi-jobs`) |
| `GET /api/coi/[id]` | 1 | COI detail |
| `POST /api/webhooks/agentmail` | 2 | AgentMail `message.received` → Neon + Cloudinary + enqueue |
| `GET /api/jobs` | 2 | List jobs with status |
| `GET /api/jobs/dlq` | 2 | List DLQ jobs (COI + reminder) |
| `POST /api/jobs/dlq/[id]/retry` | 2 | Manual retry from DLQ |
| `CRUD /api/checklist` | 3 | Checklist items |
| `GET/POST /api/coi/[id]/versions` | 3 | Version history |
| `POST /api/coi/[id]/accept` | 5 | Accept + enqueue template email |
| `POST /api/coi/[id]/reject` | 5 | Reject + enqueue template email |
| `CRUD /api/templates` | 5 | Email templates |
| `GET /api/metrics` | 6 | Compliance dashboard data |

---

## Phased Roadmap

Each phase delivers a working increment. 2–3 features per phase, ordered by dependency and complexity.

---

### Phase 1 — Foundation

**Complexity: Low · Estimated: 1–2 weeks**

| # | Feature | Deliverable |
|---|---------|-------------|
| 1 | Admin login | Secure single-admin auth in Next.js (UI + API routes) with JWT |
| 2 | Neon DB + Cloudinary | Schema design, COI record model, file upload to Cloudinary |
| 3 | Basic COI dashboard | Upload COI, list all submissions, view document, basic status |

**Problem solved:** Admin can log in, upload a COI, and see it stored securely. No more lost PDFs in email threads.

**Exit criteria:** Upload a PDF → appears in dashboard → opens from Cloudinary URL.

---

### Phase 2 — Intake & Job Queue

**Complexity: Medium · Estimated: 1–2 weeks**

| # | Feature | Deliverable |
|---|---------|-------------|
| 1 | AgentMail webhook | `maniranjan@agentmail.to` receives emails + attachments → Neon + Cloudinary |
| 2 | BullMQ pipeline | Dashboard upload and email intake both enqueue `process-coi` on `coi-jobs` |
| 3 | Job status UI | Queued / Processing / Ready / Failed / DLQ on dashboard |
| 4 | Exponential backoff | Shared retry config on all `coi-jobs` enqueues (5 attempts, 5s base) |
| 5 | Dead Letter Queue | Failed jobs → `coi-jobs-dlq`; dashboard DLQ view + optional manual retry |
| 6 | Stub worker | Worker simulates Processing → Ready (full AI in Phase 4) |
| 7 | Intake source tags | Dashboard badges show **Dashboard Upload** vs **Email (AgentMail)** per COI |

**Problem solved:** Tenants can email COIs directly. Both intake channels feed one reliable processing queue with production-grade failure handling. Admins can see at a glance where each COI came from.

**Exit criteria:**
- Email a COI to the inbox → COI record + job on dashboard → status updates
- Dashboard upload enqueues `coi-jobs` (same path as webhook)
- Each COI shows an intake source badge: **Dashboard Upload** or **Email (AgentMail)**
- Force worker failure → see exponential retries in logs
- After max attempts → job in `coi-jobs-dlq` + visible on dashboard

**Key files:** `app/api/webhooks/agentmail/`, `lib/queue/`, `lib/workers/`, `scripts/worker.ts`, `components/ui/intake-source-badge.tsx`, `docs/PHASE2.md`

**AgentMail email intake (local dev):**

Dashboard upload works without ngrok. **Email intake** requires a public webhook URL:

1. Run `npm run dev`, `npm run worker`, and `ngrok http 3000`
2. In the **AgentMail dashboard**, register:
   ```
   https://<your-ngrok-domain>/api/webhooks/agentmail
   ```
   Event: `message.received`
3. Email a **PDF attachment** to `maniranjan@agentmail.to`
4. Refresh `/dashboard` — COI appears with **Email (AgentMail)** source badge

**Intake source tags:** Every COI shows where it was received:

| Badge | Meaning | Set when |
|-------|---------|----------|
| **Dashboard Upload** (blue) | Manual upload from admin UI | `POST /api/coi` |
| **Email (AgentMail)** (teal) | Inbound email via webhook | `POST /api/webhooks/agentmail` |

Visible on **COI Dashboard**, **COI detail** (with sender email for email intake), and **Job Queue**.

| Config | Format |
|--------|--------|
| `.env` `WEBHOOK_DOMAIN` | Domain only, no `https://` (optional) |
| AgentMail webhook URL | Full `https://` URL + `/api/webhooks/agentmail` |

Full setup, test steps, and troubleshooting: **[docs/PHASE2.md](docs/PHASE2.md)**

---

### Phase 3 — Checklist & Versioning

**Complexity: Medium · Estimated: 1–2 weeks**

| # | Feature | Deliverable |
|---|---------|-------------|
| 1 | Editable checklist | Admin UI to add, edit, delete requirements with mandatory flags and categories |
| 2 | COI versioning | Per-sender version history (v1, v2, v3), compare versions side by side |
| 3 | Job-to-version linking | Every queue job tied to correct sender and version number |

**Problem solved:** Repeat submissions from the same tenant are tracked cleanly. Landlord defines compliance rules once.

**Exit criteria:** Reject v1 → tenant resubmits → v2 appears linked to same sender with full history.

---

### Phase 4 — Multi-Agent AI Pipeline

**Complexity: High · Estimated: 2–3 weeks · Branch: `phase-4`**

| # | Feature | Deliverable |
|---|---------|-------------|
| 1 | **Pre-OCR intake checks** | No PDF → auto Missing Attachment email; unreadable file → auto Processing Error |
| 2 | **LlamaParse OCR** | Extract text from COI PDF (Cloudinary) + email body |
| 3 | **Five-agent pipeline** | Document → Extraction → Checklist → Risk → Report (Groq via OpenAI SDK) |
| 4 | **Per-agent guardrails** | Input + output guardrails on every agent (OpenAI Agents SDK); tripwire stops pipeline |
| 5 | **JSON validation** | Zod schemas for every agent output; retry + Groq fallback on failure |
| 6 | **Checklist grounding** | PASS / FAIL / MISSING only (never UNKNOWN); DB checklist is source of truth |
| 7 | **Groq model fallback** | Primary → fallback 1 → fallback 2 on 429/503/unavailable only (not task-based routing) |
| 8 | **Logfire observability** | Full trace per COI job: OCR, guardrails, agents, validation, fallback events |
| 9 | **Database persistence** | `AiRun`, `AgentStep`, extracted fields + draft report on `CoiVersion` |
| 10 | **Worker integration** | Replace stub `process-coi` with real pipeline; status → Ready for Review / Failed |
| 11 | **Dashboard AI results** | Extraction JSON, checklist table, risks, draft report, agent step timeline |
| 12 | **Hybrid auto-email** | Auto-send: Missing Attachment, Processing Error, Receipt Acknowledged; admin-review cases store draft for Phase 5 |

**Problem solved:** 20-minute manual review becomes a 2-minute admin confirmation. Every clause checked consistently against the same checklist, with guardrails, structured outputs, and full observability.

**Exit criteria:**
- Email with no attachment → auto Missing Attachment (no agents)
- Upload valid COI → LlamaParse → 5 agents → 10 guardrails → dashboard shows full results
- Missing clauses → Agents 4 & 5 still run → draft report with citations stored
- Logfire shows one trace per job; Groq fallback visible on rate limit

**Key files:** `lib/ai/`, `lib/workers/process-coi.ts`, `docs/PHASE4.md`

**Not in Phase 4:** Admin report edit UI, Accept/Reject buttons, editable templates, final AgentMail send after admin edit (Phase 5).

---

### Phase 5 — Review & Email Automation

**Complexity: Medium–High · Estimated: 1–2 weeks**

| # | Feature | Deliverable |
|---|---------|-------------|
| 1 | **Editable draft report** | Admin edits Agent 5 summary, missing items, citations, tenant message before send |
| 2 | **Admin accept/reject** | Decision with mandatory rejection reason per version |
| 3 | **Editable email templates** | All 8 templates with placeholders, live preview in admin |
| 4 | **Send via AgentMail** | Output guardrail on admin-final text → template render → send |
| 5 | **Hybrid email completion** | Admin Send for: not-a-COI, guardrail fail, missing clauses, all-pass awaiting review |

**Problem solved:** Tenants get clear, specific, citation-backed feedback. Admin controls final wording before any email leaves the system.

**Exit criteria:** Admin edits draft → sends Clauses Missing email → tenant resubmits → admin accepts → Approved email with matched checklist summary.

---

### Phase 6 — Renewal, Metrics & Audit

**Complexity: Medium · Estimated: 1–2 weeks**

| # | Feature | Deliverable |
|---|---------|-------------|
| 1 | Expiry + renewal reminders | node-cron → `reminder-jobs` at 30/14/7/3 days; worker sends via AgentMail; failures → `reminder-jobs-dlq` |
| 2 | Metrics dashboard | Compliance %, ROI, savings, turnaround, automation % with live calculations |
| 3 | Full audit log | Immutable files, agent steps, emails, decisions, checklist/template changes |
| 9 | Worker concurrency | `WORKER_COI_CONCURRENCY` / `WORKER_REMINDER_CONCURRENCY` tune parallel job processing |
| 10 | Email rate limiting | BullMQ limiter caps reminder sends (`REMINDER_EMAIL_RATE_LIMIT_MAX` per window) |
| 11 | Distributed lock renewal | Token-based Redis lock with TTL renewal prevents duplicate cron scans |
| 12 | Retry + jitter | Exponential backoff with 25% jitter on both COI and reminder workers |
| 13 | Queue monitoring | `GET /api/queues/metrics` + live panel on `/dashboard/jobs` |
| 14 | Health endpoints | Public `/api/health`, `/database`, `/redis`, `/queue` for uptime probes |
| 15 | Structured logging | Cron + reminder events to console/Logfire; `CronScanLog` persisted per run |
| 16 | DLQ dashboard | Filter COI vs reminder DLQ, retry, dismiss, cron scan history table |

**Problem solved:** No more lapsed coverage surprises. Landlord sees portfolio compliance health, quantified ROI, and full operational visibility into queues and cron runs.

**Exit criteria:** COI nearing expiry triggers reminder emails → metrics dashboard reflects live compliance state → full audit trail retrievable per COI → queue health and DLQ triage available on Jobs dashboard.

See **[docs/PHASE6.md](docs/PHASE6.md)** for setup, env vars, API reference, and verify steps.

---

### Roadmap at a Glance

```
Phase 1          Phase 2          Phase 3          Phase 4                    Phase 5              Phase 6
────────         ────────         ────────         ────────                   ────────             ────────
Admin Login      AgentMail        Editable         LlamaParse OCR             Edit draft report    node-cron →
Neon +           Webhook          Checklist        5 agents + guardrails      Accept/Reject        reminder-jobs
Cloudinary       coi-jobs + DLQ   COI Versioning   Zod + Groq fallback        Email templates      Metrics
Basic Dashboard  Job Status UI    Job Linking      Logfire + AiRun/AgentStep  AgentMail send       Audit Log
                                                     Hybrid auto-email
```

**Total estimated timeline: 8–12 weeks** for a production-ready v1.

---

## Success Criteria

| Goal | Target |
|------|--------|
| COI review time reduction | > 70% vs manual PDF review |
| Automatic expiry reminders | 100% of active COIs monitored |
| Centralized compliance tracking | Single dashboard for entire portfolio |
| Executive visibility | Live metrics without spreadsheets |
| Complete audit history | Every action logged and retrievable |
| Manual intervention | Minimal — admin only approves/rejects |
| Tenant communication | Automated, specific, templated emails for every case |
| Version tracking | Full history per sender, no lost submissions |

---

## Getting Started

### Prerequisites

- Node.js 20+
- Neon PostgreSQL account ([neon.tech](https://neon.tech))
- Cloudinary account ([cloudinary.com](https://cloudinary.com))
- Redis instance (local or cloud — for BullMQ)
- Groq API key ([console.groq.com](https://console.groq.com))
- LlamaCloud / LlamaParse API key ([cloud.llamaindex.ai](https://cloud.llamaindex.ai)) — Phase 4
- Logfire account ([logfire.pydantic.dev](https://logfire.pydantic.dev)) — Phase 4
- AgentMail account with inbox `maniranjan@agentmail.to`

### Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/coi_db?sslmode=require

# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Redis / BullMQ (Phase 2+)
REDIS_URL=redis://localhost:6379
BULLMQ_COI_QUEUE=coi-jobs
BULLMQ_COI_DLQ=coi-jobs-dlq
BULLMQ_REMINDER_QUEUE=reminder-jobs
BULLMQ_REMINDER_DLQ=reminder-jobs-dlq
JOB_MAX_ATTEMPTS=5
JOB_BACKOFF_DELAY_MS=5000

# Scheduler (Phase 6)
CRON_SCHEDULE=0 9 * * *
REMINDER_DAYS_BEFORE=30,14,7,3
MANUAL_REVIEW_MINUTES=20
HOURLY_RATE_USD=45
PLATFORM_COST_ANNUAL_USD=1200

# Ops — worker concurrency, rate limits, cron lock (Phase 6)
WORKER_COI_CONCURRENCY=2
WORKER_REMINDER_CONCURRENCY=3
REMINDER_EMAIL_RATE_LIMIT_MAX=100
REMINDER_EMAIL_RATE_LIMIT_MS=60000
CRON_LOCK_TTL_SECONDS=1800

# AI — Groq via OpenAI SDK (Phase 4+)
GROQ_API_KEY=gsk_xxx
GROQ_BASE_URL=https://api.groq.com/openai/v1
GROQ_MODEL_PRIMARY=llama-3.3-70b-versatile
GROQ_MODEL_FALLBACK_1=llama-3.1-8b-instant
GROQ_MODEL_FALLBACK_2=mixtral-8x7b-32768
GROQ_GUARDRAIL_MODEL=llama-3.1-8b-instant
AI_MAX_RETRIES=2
AI_REQUEST_TIMEOUT_MS=60000

# OCR — LlamaParse (Phase 4+)
LLAMA_CLOUD_API_KEY=llx-xxx
LLAMAPARSE_TIER=agentic

# Observability — Logfire (Phase 4+)
LOGFIRE_TOKEN=your_write_token
LOGFIRE_SERVICE_NAME=coi-email-agent
LOGFIRE_ENVIRONMENT=development
LOGFIRE_SEND_TO_LOGFIRE=if-token-present

# AgentMail
AGENTMAIL_API_KEY=your_agentmail_key
INBOX_ID=maniranjan@agentmail.to
WEBHOOK_DOMAIN=your-ngrok-or-production-domain

# Auth
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_PASSWORD_HASH=bcrypt_hash_here
JWT_SECRET=your_jwt_secret

# App
PORT=3000
```

### Run Locally

```bash
# 1. Start Redis
redis-server

# 2. Next.js app (frontend + API routes)
npm install
npx prisma migrate dev
npm run dev

# 3. BullMQ worker — coi-jobs + reminder-jobs (separate terminal)
npm run worker

# 4. node-cron — enqueues reminder-jobs only (separate terminal, Phase 6)
npm run cron

# Optional: run one expiry scan immediately
npm run cron:now

# Ops smoke test (health, lock, queue metrics — Phase 6)
npm run test:ops

# 5. AgentMail webhook tunnel (separate terminal — email intake only)
# Use a reserved static domain so the URL never changes:
ngrok http 3000 --domain=your-subdomain.ngrok-free.app
# Register once in AgentMail dashboard:
# https://your-subdomain.ngrok-free.app/api/webhooks/agentmail
```

See **[docs/PHASE2.md](docs/PHASE2.md)** for AgentMail webhook setup, static ngrok domain, email test flow, and troubleshooting. Phase 4 setup: **[docs/PHASE4.md](docs/PHASE4.md)** (when available).

### Legacy prototype

The `agent.py` file is an older Flask prototype. Phase 2 email intake is implemented in Next.js at `app/api/webhooks/agentmail/` using the `agentmail` npm SDK.

---

## Project Structure

```
coi-platform/
├── app/
│   ├── (auth)/login/              # Admin login page
│   ├── dashboard/                 # COI list, search, filter
│   ├── coi/[id]/                  # COI detail, versions, AI results
│   ├── checklist/                 # Editable checklist management
│   ├── templates/                 # Email template editor
│   ├── metrics/                   # Compliance dashboard
│   └── api/                       # Backend API routes
│       ├── auth/                  # Login, session
│       ├── coi/                   # Upload, list, accept/reject
│       ├── jobs/                  # Job list, DLQ, retry (Phase 2)
│       ├── checklist/             # CRUD checklist items
│       ├── templates/             # CRUD email templates
│       └── webhooks/
│           └── agentmail/         # AgentMail inbound webhook
├── components/                    # shadcn/ui components
├── lib/
│   ├── queue/                     # Redis connection, queue definitions, enqueue helpers
│   ├── workers/                   # process-coi, send-template-email, send-reminder handlers
│   ├── cron/                      # node-cron expiry scan → reminder-jobs (Phase 6)
│   ├── observability/             # Structured logging + Logfire (Phase 6)
│   ├── agents/                    # AI agent chain (1–5)
│   ├── services/                  # Cloudinary, email, DB helpers
│   └── auth.ts                    # JWT helpers
├── prisma/
│   └── schema.prisma              # Neon PostgreSQL schema
├── docs/
│   ├── PHASE1.md                  # Phase 1 run & verify
│   ├── PHASE2.md                  # Phase 2 run & verify
│   └── PHASE6.md                  # Phase 6 renewal, metrics, ops
├── scripts/
│   ├── worker.ts                  # BullMQ worker (coi-jobs + reminder-jobs)
│   ├── cron.ts                    # node-cron entry (enqueue reminder-jobs only)
│   └── test-ops-features.ts       # Ops smoke test (Phase 6)
├── agent.py                       # Phase 2 prototype (to be replaced)
├── .env
└── README.md
```

---

## Why This Matters

Landlords with multiple properties are **underinsured against their own tenants' insurance gaps**. The COI is the only proof of coverage — and today, verifying it is a manual, error-prone, unscalable process.

This platform turns that process into:

- **Minutes instead of hours** per renewal cycle
- **Zero missed expiries** with automated reminders
- **Consistent enforcement** of your checklist on every document
- **Clear tenant communication** with specific, actionable feedback
- **Full audit trail** for lenders, HOAs, legal disputes, and compliance audits
- **Quantified ROI** so you know exactly what manual work costs

**Define your rules once. Let the system enforce them forever.**

---

*Built for landlords who have better things to do than open PDFs all day.*
