# ComplianceHub — Hybrid PDF Extraction & AI Optimization

## Goal

The main idea from the DevRev PDF extraction approach is:

> **Do not use an expensive AI/VLM model when a cheaper and reliable method can solve the problem.**

For ComplianceHub, this means:

```text
Uploaded COI PDF
      ↓
Cheap PDF checks
      ↓
Can we safely extract the text without AI?
      ↓
   ┌──┴──┐
  YES    NO
   ↓      ↓
Fast     OCR/VLM
Path     Path
   ↓      ↓
   └──┬───┘
      ↓
Validation
      ↓
Compliance extraction
      ↓
Rules / Checklist
      ↓
Compliance Report
      ↓
Human Review if needed
```

The DevRev system uses this same general principle: native PDF extraction for safe pages and VLM/OCR only when necessary. Their production system routed roughly 27% of pages through the native path and reported about 240× lower latency for that path, while keeping accuracy within roughly 2–3% of the all-OCR baseline.

---

# 1. First: Understand the Problem

A COI can be:

### Type A — Digital PDF

Example:

```text
Certificate Holder: ABC Properties
Insured: XYZ Construction
Policy Number: POL-12345
Expiration Date: 12/31/2026
General Liability: $1,000,000
```

The text is already inside the PDF.

You don't need a VLM just to read it.

### Type B — Scanned PDF

The PDF may actually contain:

```text
[IMAGE OF COI]
```

There may be no useful embedded text.

Here OCR/VLM is useful.

### Type C — Complex PDF

For example:

```text
Text
        ┌───────────────┐
        │     TABLE     │
        └───────────────┘

Formula / image / complex layout
```

Native text extraction may not understand the structure.

These documents should go through the AI/VLM path.

---

# 2. Current Problem in a Traditional Pipeline

A simple implementation might do:

```text
PDF
 ↓
OCR / VLM
 ↓
Extract fields
 ↓
Compliance check
```

This works, but you're potentially doing:

```text
Simple digital PDF
        ↓
expensive AI
        ↓
extract text
```

That's unnecessary.

The better architecture is:

```text
PDF
 ↓
Pre-processing
 ↓
Eligibility / Routing
 ↓
 ┌───────────────────┐
 │                   │
 ↓                   ↓
FAST PATH          AI PATH
 │                   │
PyMuPDF             OCR/VLM
 │                   │
 └─────────┬─────────┘
           ↓
      Normalized text
           ↓
     Extraction Agent
           ↓
    Validation Agent
           ↓
      Rules Engine
           ↓
   Compliance Report
```

---

# 3. The Most Important Concept: Fast Path + Slow Path

## Fast Path

Use normal deterministic tools.

For example:

```text
PyMuPDF
PDF parser
regex
coordinate extraction
```

Advantages:

- very fast
- cheap
- no GPU
- deterministic
- easier to debug

## Slow Path

Use AI only when necessary.

For example:

```text
OCR
VLM
LLM
```

Advantages:

- handles scans
- understands layouts
- handles tables
- handles complicated documents
- can interpret visual information

---

# 4. How to Implement This in ComplianceHub

## Recommended Architecture

```text
                         USER
                           │
                           ↓
                    Upload COI PDF
                           │
                           ↓
                       Cloudinary
                           │
                           ↓
                     Ingestion API
                           │
                           ↓
                  Document Processing Job
                           │
                           ↓
                 ┌─────────────────────┐
                 │ PDF Pre-Processor   │
                 └──────────┬──────────┘
                            ↓
                   PDF Eligibility Gate
                            │
                    ┌───────┴────────┐
                    ↓                ↓
                FAST PATH         AI PATH
                    ↓                ↓
                PyMuPDF           OCR/VLM
                    ↓                ↓
                    └───────┬────────┘
                            ↓
                    Normalized Document
                            ↓
                   Extraction Agent
                            ↓
                  Validation Agent
                            ↓
                  Compliance Agent
                            ↓
                    Rules Engine
                            ↓
                Compliance Report
                            ↓
              ┌─────────────┴────────────┐
              ↓                          ↓
          High confidence             Uncertain
              ↓                          ↓
          Auto-process             Human Review
```

---

# 5. Where This Fits in Your Existing 5-Agent System

Your existing ComplianceHub idea has multiple agents around:

1. Document/security validation
2. Extraction
3. Checklist/rules
4. Compliance/report
5. Email/review

Don't replace that architecture.

Instead, add a **routing layer BEFORE the extraction agent**.

```text
                PDF
                 ↓
       Document Security Check
                 ↓
       Hybrid Extraction Router
                 ↓
       ┌─────────┴─────────┐
       ↓                   ↓
   Native Path          VLM/OCR Path
   (PyMuPDF)             (AI)
       ↓                   ↓
       └─────────┬─────────┘
                 ↓
          Extraction Agent
                 ↓
          Validation Agent
                 ↓
           Rules Engine
                 ↓
        Compliance Agent
                 ↓
       Human Review / Email
```

This is important:

> **Hybrid extraction is an optimization layer, not a replacement for your existing compliance architecture.**

---

# 6. Build an Extraction Router

Create something conceptually like:

```python
def choose_extraction_path(pdf):
    if is_safe_for_native_extraction(pdf):
        return "native"

    return "vlm"
```

Then:

```python
path = choose_extraction_path(pdf)

if path == "native":
    text = extract_with_pymupdf(pdf)
else:
    text = extract_with_vlm(pdf)
```

This is the basic version.

Later, make the routing more sophisticated.

---

# 7. Eligibility Gate

The router should be conservative.

The DevRev implementation used four major checks before allowing native extraction.

For ComplianceHub, use a similar gate.

```text
             PDF PAGE
                ↓
        ┌─────────────────┐
        │ Check 1         │
        │ Text-only?      │
        └────────┬────────┘
                 ↓
             PASS?
           ┌─────┴─────┐
          YES          NO
           ↓            ↓
        Check 2        VLM
           ↓
        Check 3
           ↓
        Check 4
           ↓
      Native extraction
```

---

# 8. Check 1 — Is the Page Text-Only?

Ask:

```text
Does this page contain only normal text?
```

If:

```text
Text
Text
Text
```

→ native extraction may be safe.

If:

```text
Text
Table
Image
Formula
```

→ VLM.

The DevRev approach routes pages containing tables, formulas, or image regions to the VLM because native PDF extraction does not reconstruct those structures properly.

### ComplianceHub example

Suppose a COI contains:

```text
Insured:
ABC Construction

Policy information:
...

Coverage table:
┌───────────────┬───────────┐
│ Coverage      │ Amount    │
├───────────────┼───────────┤
│ General Liab. │ $1M       │
└───────────────┴───────────┘
```

Don't blindly trust native extraction.

Send the complex page to the VLM.

---

# 9. Check 2 — Does It Contain Enough Text?

A page containing:

```text
Page 1
```

is technically extractable.

But it isn't useful.

So establish a minimum text threshold.

The DevRev article used:

```text
embedded characters >= 8
```

as one conservative check.

For ComplianceHub, you can start with a similar threshold and tune it using your own COI dataset.

Important:

> Don't assume the threshold is universally correct. Measure it against your documents.

---

# 10. Check 3 — Is the Text Real Embedded Text?

This is one of the smartest ideas from the article.

Some scanned PDFs have hidden OCR text.

So the PDF may look like:

```text
[SCANNED IMAGE]
```

but internally contain:

```text
IMAGE
+
OCR TEXT LAYER
```

The OCR text may be inaccurate.

Therefore:

```text
PDF text exists
      ↓
Is it genuinely visible?
      ↓
YES → Native extraction
NO  → VLM
```

The DevRev implementation examined PDF text rendering modes and used a 70% visible-text threshold to distinguish likely genuine embedded text from OCR overlays.

For ComplianceHub:

```text
visible_text_ratio >= threshold
        ↓
       SAFE

visible_text_ratio < threshold
        ↓
       VLM
```

Start conservatively.

Then evaluate.

---

# 11. Check 4 — Validate Word-to-Region Assignment

This is especially useful for avoiding silent extraction errors.

Concept:

```text
Layout detector:
Region A
Region B
Region C

Extracted words:
A B C X
      ↑
    unknown
```

If a word cannot be assigned to a known region:

```text
Possible layout mismatch
        ↓
Don't trust native extraction
        ↓
Fallback to VLM
```

This follows the DevRev approach of checking whether extracted words can be consistently assigned to detected regions.

---

# 12. Why You Should NOT Start With Region-Level Routing

You may be tempted to build:

```text
Text region → PyMuPDF
Table → VLM
Image → VLM
Formula → VLM
```

Theoretically this saves more AI calls.

But there is a problem.

Layout detector bounding boxes are not always perfect.

For example:

```text
Actual:

Paragraph A
Paragraph B
```

Detector:

```text
┌──────────────────┐
│ Paragraph A      │
│ Paragraph B      │
└──────────────────┘
```

Or:

```text
┌──────────────┐
│ Paragraph A  │
│ Paragraph B  │ ← accidental overlap
└──────────────┘
```

PyMuPDF will literally extract whatever coordinates fall inside the box.

This can create:

- duplicated text
- missing text
- broken ordering

The VLM is more tolerant of imperfect crops, while native extraction isn't.

Therefore:

> **Start with page-level routing.**

---

# 13. Page-Level Routing for ComplianceHub

Use:

```text
Page
 ↓
Is the entire page safe?
 ↓
YES → PyMuPDF
NO  → VLM
```

This is safer.

Example:

```text
COI Page 1
   ↓
Only text?
   ↓
YES
   ↓
Enough embedded text?
   ↓
YES
   ↓
Visible text?
   ↓
YES
   ↓
All words mapped?
   ↓
YES
   ↓
PyMuPDF
```

But:

```text
COI Page 2
   ↓
Contains table
   ↓
NO
   ↓
VLM
```

Even if 80% of Page 2 is text, send the entire page to VLM initially.

This sacrifices some theoretical savings in exchange for correctness.

---

# 14. Add Confidence to ComplianceHub

Another important technique:

> **Don't treat every extraction result as equally trustworthy.**

For every extracted field, store something like:

```json
{
  "policy_number": {
    "value": "POL-12345",
    "confidence": 0.97,
    "source": "native"
  }
}
```

Or:

```json
{
  "policy_number": {
    "value": "POL-12345",
    "confidence": 0.71,
    "source": "vlm"
  }
}
```

Then:

```text
Confidence >= threshold
        ↓
Continue automatically

Confidence < threshold
        ↓
Verification / Human Review
```

You already have the concept of confidence thresholds and human review in your ComplianceHub architecture; this hybrid extraction layer gives you another signal to use.

---

# 15. Don't Let the LLM Make Every Decision

For ComplianceHub, separate:

### AI tasks

Use AI for:

```text
Extract:
- insured name
- policy number
- carrier
- coverage
- limits
- dates
- certificate holder
```

### Deterministic tasks

Use code/database rules for:

```text
Is policy expired?

Does GL >= required limit?

Does certificate holder match?

Is required coverage present?

Does expiration date satisfy requirement?

Is additional insured requirement satisfied?
```

Your PostgreSQL rules engine should remain the source of truth for deterministic compliance decisions.

Architecture:

```text
PDF
 ↓
Extraction
 ↓
Structured JSON
 ↓
Deterministic validation
 ↓
PostgreSQL rules
 ↓
Compliance decision
```

This is much safer than asking an LLM:

> "Is this COI compliant?"

---

# 16. Add Evidence to Every Extracted Field

For ComplianceHub, this is extremely valuable.

Instead of:

```json
{
  "policy_limit": "$1,000,000"
}
```

store:

```json
{
  "policy_limit": {
    "value": "$1,000,000",
    "page": 2,
    "source": "native",
    "confidence": 0.98
  }
}
```

For VLM extraction:

```json
{
  "policy_limit": {
    "value": "$1,000,000",
    "page": 2,
    "source": "vlm",
    "confidence": 0.91,
    "evidence": "General Liability - $1,000,000"
  }
}
```

This lets the reviewer answer:

> "Where did this value come from?"

without manually searching the whole document.

---

# 17. Hybrid Extraction + Your Existing Guardrails

Your pipeline should look like:

```text
                    PDF
                     ↓
             Security Guardrail
                     ↓
           Prompt Injection Check
                     ↓
              PDF Preprocessing
                     ↓
            Hybrid Router
             ↙         ↘
        Native           VLM
        Path             Path
          ↓                ↓
          └───────┬────────┘
                  ↓
          Structured Output
                  ↓
           Schema Validation
                  ↓
          Evidence Validation
                  ↓
         Confidence Evaluation
                  ↓
         Deterministic Rules
                  ↓
           Compliance Result
                  ↓
       ┌──────────┴─────────┐
       ↓                    ↓
    Compliant           Review Needed
       ↓                    ↓
    Continue            Human Review
```

---

# 18. Use Strict Structured Output

Never let the extraction agent return random text.

Use a schema.

For example:

```json
{
  "insured_name": "...",
  "carrier": "...",
  "policy_number": "...",
  "effective_date": "...",
  "expiration_date": "...",
  "coverages": [],
  "limits": [],
  "certificate_holder": "...",
  "additional_insured": false,
  "evidence": []
}
```

Then validate it.

```text
LLM/VLM output
      ↓
Pydantic/schema validation
      ↓
Valid?
 ┌────┴────┐
YES        NO
 ↓          ↓
Continue   Retry/Fallback
```

---

# 19. Add a Fallback Chain

Don't have only:

```text
Native → VLM
```

You can eventually build:

```text
                  PDF
                   ↓
              Native parser
                   ↓
             Valid result?
              ↙       ↘
            YES        NO
             ↓          ↓
           Done       OCR/VLM
                         ↓
                   Valid result?
                    ↙       ↘
                  YES        NO
                   ↓          ↓
                 Done      Human Review
```

This gives you graceful failure.

---

# 20. Important Production Principle: "Worst Case Should Not Become Worse"

This is one of the strongest ideas from the DevRev implementation.

The fast path should be an **optimization**, not a dependency.

Meaning:

```text
If fast path succeeds:
    Great → save time/cost

If fast path fails:
    VLM handles it
```

Therefore:

```text
Before:
PDF → VLM

After:
PDF → Fast Path → if unsafe → VLM
```

The system should never become less capable just because you introduced the optimization.

---

# 21. Idempotency

This is very important for your BullMQ/Inngest processing.

Suppose the same PDF gets processed twice.

Don't run:

```text
VLM
VLM
VLM
```

again unnecessarily.

Create a document-processing key:

```text
document_id + file_hash + pipeline_version
```

Example:

```text
doc_123
+
sha256(pdf)
+
v2
```

Before processing:

```text
Already processed?
     ↓
   YES → return existing result
   NO  → process
```

This saves both time and AI cost.

---

# 22. Cache Extraction Results

If the same document is uploaded again:

```text
PDF hash
   ↓
Redis / PostgreSQL
   ↓
Existing extraction?
   ↓
YES → reuse
NO  → process
```

This is another form of:

> **Don't pay twice for the same work.**

---

# 23. Use Document-Level and Page-Level Hashes

You can make this even better.

Instead of only:

```text
document_hash
```

use:

```text
document_hash
+
page_hash
```

Then:

```text
Document
 ├── Page 1 → hash A
 ├── Page 2 → hash B
 ├── Page 3 → hash C
```

If only Page 3 changes:

```text
Page 1 → reuse
Page 2 → reuse
Page 3 → process
```

This can become very useful when documents are re-uploaded with small modifications.

---

# 24. Use Model Routing

The same idea doesn't have to stop at PDF extraction.

You can eventually have:

```text
Easy
 ↓
Rules / parser

Medium
 ↓
Small/cheap model

Hard
 ↓
Powerful VLM/LLM
```

For ComplianceHub:

```text
Simple digital COI
        ↓
PyMuPDF

Normal scanned COI
        ↓
OCR

Very complex COI
        ↓
VLM
```

This is called **model routing**.

---

# 25. Add an LLM Budget

You can also monitor:

```text
How many AI calls per document?
How many tokens?
How many pages?
How much latency?
How much cost?
```

Example:

```text
Document
  ↓
20 pages
  ↓
15 native
5 VLM
```

Instead of:

```text
20 pages
  ↓
20 VLM calls
```

Your observability should show this.

---

# 26. Observability You Should Add

Since you are already thinking about Logfire/Phoenix/LangSmith-style observability, add these metrics.

### Per document

```text
document_id
page_count
native_pages
vlm_pages
fallback_pages
failed_pages
total_latency
extraction_latency
validation_latency
```

### AI metrics

```text
VLM calls
LLM calls
tokens
model
latency
retries
failures
```

### Accuracy

```text
field accuracy
validation failures
human corrections
fallback rate
```

---

# 27. Very Important Metrics

Track:

## Fast-path rate

```text
native pages / total pages
```

Example:

```text
30 / 100 = 30%
```

## VLM rate

```text
VLM pages / total pages
```

## Fallback rate

```text
native attempts that failed validation
/
native attempts
```

## Accuracy

```text
correct fields / total fields
```

## Latency

Track:

```text
P50
P95
P99
```

Don't only look at average latency.

---

# 28. Example ComplianceHub Metrics Dashboard

```text
------------------------------------
ComplianceHub Extraction
------------------------------------

Documents processed:       10,000

Pages processed:           80,000

Native extraction:         28,000
VLM extraction:             52,000

Fast-path rate:               35%

Native fallback rate:          2%

Average latency:              1.8s
P95 latency:                  5.2s

Average VLM calls/doc:         3.1

Extraction accuracy:         97.8%

Human review rate:             4.2%
------------------------------------
```

This gives you actual evidence that the optimization works.

---

# 29. Don't Optimize Before Measuring

First build:

```text
Baseline:
Everything → VLM
```

Measure:

```text
latency
cost
accuracy
GPU/API usage
failure rate
```

Then add hybrid routing.

Measure again.

Compare:

```text
                BEFORE       AFTER

Latency          10 sec       3 sec
VLM calls        10            4
Cost             $X           $0.4X
Accuracy         98%           97.5%
Fallback         --             3%
```

Now you can confidently say:

> "We reduced model usage while keeping accuracy within our acceptable threshold."

---

# 30. Start Conservative

Don't immediately try to maximize fast-path coverage.

Start:

```text
Only very safe pages
        ↓
Native extraction
```

For example:

```text
100 pages

10 → native
90 → VLM
```

Then evaluate.

If accuracy is good:

```text
10 → 20 → 30 → 40
```

Gradually increase coverage.

This is much safer than:

```text
Let's route 80% to native immediately.
```

---

# 31. Use Human Review as a Safety Net

Your ComplianceHub architecture already benefits from human review.

Use:

```text
High confidence
      ↓
Automatic decision
```

But:

```text
Low confidence
OR
validation failure
OR
conflicting evidence
      ↓
Human Review
```

Example:

```text
Policy limit extracted:
$1M

Required:
$2M

Confidence:
0.96
```

This isn't an extraction problem.

It's a deterministic compliance failure.

→ Mark non-compliant.

But:

```text
Policy limit:
"$1,0??,000"

Confidence:
0.54
```

→ Human review.

---

# 32. Important Distinction: Extraction vs Compliance

Keep these separate.

### Extraction asks:

> "What does the document say?"

### Compliance asks:

> "Does what the document says satisfy our requirements?"

Architecture:

```text
PDF
 ↓
Extraction
 ↓
"What does it say?"
 ↓
Structured JSON
 ↓
Rules Engine
 ↓
"Does it comply?"
```

This separation makes your system easier to debug.

---

# 33. Example End-to-End COI

Suppose a property manager uploads:

```text
COI.pdf
```

### Step 1

Cloudinary stores the immutable PDF.

```text
Cloudinary
    ↓
document_id
```

### Step 2

Create processing job.

```text
document_id
status = PROCESSING
```

### Step 3

Run security/document validation.

```text
Safe?
 ↓
YES
```

### Step 4

Hybrid router examines pages.

```text
Page 1 → native
Page 2 → native
Page 3 → VLM
Page 4 → native
```

### Step 5

Extraction results are normalized.

```json
{
  "insured": "ABC Construction",
  "policy_number": "POL123",
  "expiration": "2026-12-31",
  "general_liability": "$1M"
}
```

### Step 6

Validation checks:

```text
Schema valid?
Evidence exists?
Confidence acceptable?
Dates valid?
```

### Step 7

PostgreSQL rules:

```text
Required GL = $2M
Actual GL = $1M

→ FAIL
```

### Step 8

Compliance report:

```text
Status: NON-COMPLIANT

Reason:
General Liability limit below required amount.

Evidence:
Page 2
```

### Step 9

Human review/email workflow if required.

---

# 34. How to Implement It Incrementally

Don't rebuild ComplianceHub all at once.

## Phase 1 — Baseline

Keep your existing pipeline.

Measure:

```text
latency
cost
accuracy
VLM calls
```

---

## Phase 2 — Add PyMuPDF

Add:

```text
PDF
 ↓
PyMuPDF
 ↓
Can we extract meaningful text?
```

Don't automatically trust it yet.

---

## Phase 3 — Add Routing

```text
Safe
 ↓
PyMuPDF

Unsafe
 ↓
VLM
```

---

## Phase 4 — Add Validation

```text
Native extraction
 ↓
Validation
 ↓
Pass → use result
Fail → VLM
```

This is extremely important.

---

## Phase 5 — Add Confidence

```text
confidence >= threshold
       ↓
automatic

confidence < threshold
       ↓
review
```

---

## Phase 6 — Add Observability

Track:

```text
native rate
VLM rate
fallback rate
latency
accuracy
cost
```

---

## Phase 7 — Optimize Further

Only after you have enough production data consider:

```text
mixed-page routing
region-level routing
small model routing
caching
page-level reuse
```

---

# 35. Future Optimization: Mixed-Page Routing

Currently:

```text
Page:

80% text
20% table

        ↓

Entire page → VLM
```

This is safe but potentially expensive.

Future architecture:

```text
Page
 ├── Text → PyMuPDF
 ├── Table → VLM
 └── Image → VLM
```

But only do this once your layout detector is reliable enough.

The DevRev article identifies mixed-page routing as a future direction as layout detection improves.

---

# 36. The General Engineering Pattern

You should remember this architecture:

```text
                 INPUT
                   ↓
             CHEAP CHECK
                   ↓
          ┌────────┴────────┐
          ↓                 ↓
       EASY               HARD
          ↓                 ↓
    Deterministic         AI
       method             model
          ↓                 ↓
          └────────┬────────┘
                   ↓
              VALIDATION
                   ↓
              CONFIDENCE
                   ↓
          ┌────────┴────────┐
          ↓                 ↓
        TRUST             REVIEW
```

This pattern is useful in almost every AI project.

---

# 37. Where Else You Can Use This Pattern

## RAG

Instead of always searching:

```text
Question
 ↓
Check cache / known answer
 ↓
If not → RAG
```

## Customer support

```text
Simple FAQ
 ↓
Database/FAQ

Complex issue
 ↓
LLM
```

## Voice agents

```text
Simple command
 ↓
Rules

Complex conversation
 ↓
LLM
```

## Fraud detection

```text
Obvious safe transaction
 ↓
Rules

Suspicious transaction
 ↓
ML model
```

## Email processing

```text
Known template
 ↓
Regex/parser

Unknown email
 ↓
LLM
```

## Document processing

```text
Digital text
 ↓
Parser

Scanned/complex
 ↓
OCR/VLM
```

---

# 38. Key Learning #1

## "Don't use AI for problems that don't require AI."

Before calling an LLM/VLM ask:

```text
Can code solve this?
Can SQL solve this?
Can regex solve this?
Can a parser solve this?
Can cached data solve this?
Can a smaller model solve this?
```

Only then:

```text
Use expensive AI.
```

---

# 39. Key Learning #2

## Fast path + fallback is a powerful architecture

```text
Fast method
    ↓
If confident → DONE
    ↓
Otherwise
    ↓
Powerful method
```

This is safer than trying to make the cheap method handle everything.

---

# 40. Key Learning #3

## More granular doesn't always mean better

You might think:

```text
region-level > page-level
```

because it gives more savings.

But:

```text
more optimization
≠
better system
```

If the input signals are noisy, a more granular decision can actually reduce correctness.

---

# 41. Key Learning #4

## Validation should be part of the architecture

Don't do:

```text
Extract → Trust
```

Do:

```text
Extract
 ↓
Validate
 ↓
Trust
```

And:

```text
Validation failure
 ↓
Fallback
```

---

# 42. Key Learning #5

## Optimize for correctness + latency + cost

A good AI system isn't:

```text
fastest possible
```

It's:

```text
Fast enough
+
Accurate enough
+
Cheap enough
+
Reliable enough
```

---

# 43. Key Learning #6

## Measure production impact

Always capture:

```text
Latency
Cost
Accuracy
Throughput
Error rate
Fallback rate
AI calls
```

Then prove the improvement.

---

# 44. Key Learning #7

## Design AI systems to degrade gracefully

Good:

```text
Fast path fails
      ↓
VLM fallback
      ↓
Human review if necessary
```

Bad:

```text
Fast path fails
      ↓
Garbage result
      ↓
Wrong compliance decision
```

---

# 45. Your Ideal ComplianceHub Architecture

Putting everything together:

```text
                         USER
                           │
                           ↓
                      COI Upload
                           │
                           ↓
                       Cloudinary
                           │
                           ↓
                    Ingestion API
                           │
                           ↓
                    Queue / Worker
                           │
                           ↓
                 Security Guardrails
                           │
                           ↓
                  PDF Pre-Processor
                           │
                           ↓
                 HYBRID ROUTER
                           │
              ┌────────────┴────────────┐
              ↓                         ↓
        SAFE DIGITAL                COMPLEX
            PAGE                      PAGE
              ↓                         ↓
          PyMuPDF                    OCR/VLM
              ↓                         ↓
              └────────────┬────────────┘
                           ↓
                 Structured Extraction
                           ↓
                  Schema Validation
                           ↓
                  Evidence Validation
                           ↓
                 Confidence Evaluation
                           ↓
                    Extraction Agent
                           ↓
               Deterministic Rules Engine
                           ↓
                  PostgreSQL Rules
                           ↓
              Compliance Decision
                           │
                 ┌─────────┴─────────┐
                 ↓                   ↓
             CONFIDENT            UNCERTAIN
                 ↓                   ↓
           Auto-process          Human Review
                 ↓                   ↓
             Report / Email / Notification
                           ↓
                     Observability
                           ↓
              Logfire / Phoenix / Metrics
```

---

# 46. What I Would Implement First in ComplianceHub

If you want the highest-value implementation without overengineering it, prioritize these:

### Priority 1 — Native PDF extraction

Add:

```text
PyMuPDF
```

for born-digital PDFs.

### Priority 2 — Routing

Build:

```text
is_safe_for_native_extraction()
```

### Priority 3 — Fallback

```text
Native → validation → VLM if failed
```

### Priority 4 — Evidence

Every extracted field should know:

```text
value
page
source
confidence
```

### Priority 5 — Deterministic rules

Keep compliance decisions in your PostgreSQL/business-rule layer.

### Priority 6 — Idempotency

Prevent the same document/page from being processed repeatedly.

### Priority 7 — Observability

Measure:

```text
native %
VLM %
fallback %
latency
accuracy
cost
```

These seven features would give you most of the value without making the architecture unnecessarily complicated.

---

# 47. A Simple Mental Model

Whenever you build an AI pipeline, think:

```text
                  "Do I really need AI?"
                           ↓
                         NO
                           ↓
                    Use cheap method
                           ↓
                       Validate
                           ↓
                         DONE

                         YES
                           ↓
                     Use AI model
                           ↓
                       Validate
                           ↓
                         DONE
```

And when you're unsure:

```text
Cheap method
    ↓
Not confident?
    ↓
AI fallback
```

---

# 48. One Sentence to Remember

> **"Use deterministic and cheap methods for easy cases, route only uncertain or complex cases to expensive AI, and always validate before trusting the result."**

That is the main engineering lesson from this PDF extraction work—and it maps very naturally onto ComplianceHub.

---

# 49. Interview Explanation

If asked:

### "How would you optimize your ComplianceHub document pipeline?"

A strong answer would be:

> "I would introduce a hybrid extraction layer before the extraction agent. First, I would inspect whether a PDF page has reliable embedded text. If it is a clean digital-text page, I would extract it directly using PyMuPDF instead of calling a VLM. For scanned or complex pages containing tables, images, or formulas, I would fall back to OCR/VLM. I would keep the routing conservative and validate native extraction before trusting it. If validation fails, the page goes to the VLM. Then I would use structured outputs, confidence scores, evidence, and deterministic PostgreSQL rules for the actual compliance decision. Finally, I'd measure fast-path rate, fallback rate, latency, accuracy, and cost to verify the optimization in production."

---

# 50. Final Checklist for ComplianceHub

Before shipping this optimization:

- [ ] Add PyMuPDF native extraction
- [ ] Build page-level eligibility gate
- [ ] Check embedded text quantity
- [ ] Detect likely OCR overlays
- [ ] Detect complex regions
- [ ] Validate native extraction
- [ ] Add VLM fallback
- [ ] Keep page-level routing initially
- [ ] Add structured extraction schema
- [ ] Add confidence scores
- [ ] Store page/evidence information
- [ ] Keep compliance rules deterministic
- [ ] Add human review for uncertain cases
- [ ] Add document/page idempotency
- [ ] Add extraction caching where appropriate
- [ ] Track native vs VLM usage
- [ ] Track P50/P95/P99 latency
- [ ] Track extraction accuracy
- [ ] Track fallback rate
- [ ] Track AI/API cost
- [ ] Add observability
- [ ] Run an offline benchmark before production rollout
- [ ] Gradually increase fast-path coverage
- [ ] Consider mixed-page routing only after validating detector quality

## The philosophy

```text
             DON'T ASK:
     "How can I make the AI faster?"

                  ASK:

     "Do I need to call the AI at all?"
```

That question can lead to some of the biggest improvements in production AI systems.
