# Deprecated for background workers.
# Background jobs now run via Inngest on the Next.js /api/inngest route.
# Use docker-compose.yml only for optional local Redis.
#
# Kept as a no-op placeholder so older docs don't break CI references.

FROM alpine:3.20
CMD ["echo", "Worker containers are obsolete. Use Inngest — see BACKGROUND_JOB_ARCHITECTURE.md"]
