import { registerOTel } from "@vercel/otel";
import { applyLogfireOtelEnv } from "@/lib/observability/otel-env";
import { shouldSendToLogfire, tryGetEnv } from "@/lib/env";

export async function register() {
  if (process.env.NEXT_RUNTIME === "edge") {
    return;
  }

  try {
    const env = tryGetEnv();
    if (!env) {
      console.warn(
        "[instrumentation] Skipping OpenTelemetry — environment validation failed (check Vercel env vars)"
      );
      return;
    }

    if (shouldSendToLogfire()) {
      applyLogfireOtelEnv();
    }

    registerOTel({
      serviceName: `${env.LOGFIRE_SERVICE_NAME}-nextjs`,
    });
  } catch (error) {
    console.error("[instrumentation] OpenTelemetry registration failed:", error);
  }
}
