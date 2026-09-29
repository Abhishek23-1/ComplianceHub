# Background Job Architecture (Inngest)

This project uses **Inngest** for all background work, event-driven workflows, and scheduled jobs.
**Redis is used only for DLQ** (plus existing rate-limits / session revocation / cron locks) — not as a job queue.

Official docs: https://www.inngest.com/docs

---

## Architecture overview

```
Vercel (Next.js)
  ├── UI + API routes
  ├── POST events via inngest.send(...)
  └── GET/POST/PUT /api/inngest   ← Inngest invokes functions here

Inngest Cloud / Dev Server
  ├── Retries (built-in)
  ├── Cron triggers
  └── Calls /api/inngest when work is due

Redis
  └── dlq:<id> + dlq:index        ← permanent failures only
```

| Concern | Technology |
|---------|------------|
| Background jobs | Inngest functions |
| Cron / schedules | Inngest `cron()` trigger |
| Retries | Inngest built-in `retries` |
| Permanent failure | Redis DLQ (`lib/dlq`) |
| Admin replay | `POST /api/admin/dlq/:id/retry` → `inngest.send` |

---

## Event flow

| Event name | Function ID | Triggered by |
|------------|-------------|--------------|
| `coi/process.requested` | `process-coi` | COI upload / AgentMail webhook |
| `coi/email.template.requested` | `send-template-email` | Accept / Reject / Send email |
| `coi/reminder.requested` | `send-reminder` | Expiry cron scan |
| Cron `CRON_SCHEDULE` | `expiry-reminder-cron` | Inngest schedule |

Enqueue from app code:

```ts
await inngest.send(processCoiRequested.create({ ... }));
```

---

## Retry flow

1. Function throws → Inngest retries automatically (default: `JOB_MAX_ATTEMPTS - 1` retries).
2. Backoff is Inngest’s official schedule (no custom retry loop).
3. After all retries fail → `onFailure` runs → write Redis DLQ + mark Neon `CoiJob` as `DLQ`.

---

## DLQ flow

Key strategy:

- `dlq:<jobId>` → JSON entry
- `dlq:index` → sorted set of ids by `failedAt`

Entry shape:

```json
{
  "id": "...",
  "eventName": "coi/process.requested",
  "payload": {},
  "error": "...",
  "stack": "...",
  "failedAt": "ISO-8601",
  "retryCount": 5,
  "executionId": "inngest-run-id",
  "metadata": {}
}
```

---

## Cron flow

1. Inngest fires `expiry-reminder-cron` on `CRON_SCHEDULE` (default `0 9 * * *`).
2. Function calls `runExpiryReminderScanOnce()` (Redis distributed lock + `CronScanLog`).
3. Scan creates reminder `CoiJob` rows and sends `coi/reminder.requested` events.
4. `send-reminder` function delivers emails via AgentMail.

---

## Replay flow

1. `GET /api/admin/dlq` — list Redis DLQ
2. `GET /api/admin/dlq/:id` — get one entry
3. `POST /api/admin/dlq/:id/retry` — validate → `inngest.send(...)` → delete Redis entry
4. `DELETE /api/admin/dlq/:id` — dismiss Redis entry

Dashboard `/dashboard/jobs` still uses:

- `GET /api/jobs/dlq`
- `POST /api/jobs/dlq/:id/retry`
- `DELETE /api/jobs/dlq/:id`

Those now also back onto Inngest + Redis DLQ.

---

## Environment variables

Official Inngest SDK variables (see https://www.inngest.com/docs/sdk/environment-variables):

| Variable | Purpose |
|----------|---------|
| `INNGEST_DEV` | `1` for local Dev Server |
| `INNGEST_EVENT_KEY` | Send events (production) |
| `INNGEST_SIGNING_KEY` | Secure `/api/inngest` (production) |
| `INNGEST_SIGNING_KEY_FALLBACK` | Key rotation |
| `INNGEST_BASE_URL` | Custom Inngest host (rarely needed) |
| `INNGEST_ENV` | Branch environments |
| `INNGEST_SERVE_ORIGIN` / `INNGEST_SERVE_PATH` | Serve URL hints |
| `INNGEST_STREAMING` | Streaming responses |
| `INNGEST_LOG_LEVEL` | SDK log level |

App-controlled:

| Variable | Purpose |
|----------|---------|
| `REDIS_URL` | DLQ + locks + rate limits |
| `JOB_MAX_ATTEMPTS` | Total attempts (Inngest retries = N−1) |
| `WORKER_COI_CONCURRENCY` | Inngest concurrency for process-coi |
| `WORKER_REMINDER_CONCURRENCY` | Inngest concurrency for reminders |
| `REMINDER_EMAIL_RATE_LIMIT_*` | Inngest throttle for reminders |
| `CRON_SCHEDULE` | Inngest cron expression |
| `REMINDER_DAYS_BEFORE` | Scan windows |
| `CRON_LOCK_TTL_SECONDS` | Redis lock TTL during scan |

Removed (obsolete): `BULLMQ_*`, `JOB_BACKOFF_DELAY_MS`, Docker worker/cron processes.

---

## Local development

```bash
# Terminal 1 — Next.js
npm run dev

# Terminal 2 — Inngest Dev Server (official CLI)
npm run inngest:dev
```

Open Inngest UI (typically http://localhost:8288) to inspect events and runs.

Set in `.env`:

```env
INNGEST_DEV=1
REDIS_URL=...
```

---

## Production (Vercel)

1. Deploy Next.js to Vercel (includes `/api/inngest`).
2. Create an Inngest app and add `INNGEST_EVENT_KEY` + `INNGEST_SIGNING_KEY` to Vercel env.
3. Sync your app in the Inngest dashboard (points at `https://your-app.vercel.app/api/inngest`).
4. No separate Docker worker/cron containers are required.

---

## Failure recovery

| Situation | Action |
|-----------|--------|
| Transient API failure | Automatic Inngest retry |
| Permanent failure | Redis DLQ + Jobs dashboard |
| Replay | Admin/dashboard retry → `inngest.send` |
| Dismiss | DELETE DLQ entry; Neon job → `FAILED` |

---

## Project layout

```
inngest/
  client.ts
  events.ts
  functions/
    process-coi.ts
    send-template-email.ts
    send-reminder.ts
    expiry-reminder-cron.ts
    index.ts
app/api/inngest/route.ts
app/api/admin/dlq/
lib/dlq/
lib/jobs/types.ts
lib/workers/          # business handlers (no BullMQ)
```
