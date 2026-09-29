import type { NextConfig } from "next";
import path from "path";

const nextConfig: NextConfig = {
  outputFileTracingRoot: path.join(__dirname),
  // Admin workspace pages must not reuse stale client RSC payloads after
  // background job / upload updates. zero = refetch on every soft navigation.
  experimental: {
    // On Windows, parallel static workers can race renaming export/500.html →
    // server/pages/500.html (ENOENT). Cap workers to keep the build stable.
    ...(process.platform === "win32" ? { cpus: 1 } : {}),
    staleTimes: {
      dynamic: 0,
      static: 0,
    },
  },
  serverExternalPackages: [
    "ioredis",
    "inngest",
    "agentmail",
    "@pydantic/logfire-node",
    "logfire",
  ],
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "res.cloudinary.com",
      },
    ],
  },
  async headers() {
    const isProd = process.env.NODE_ENV === "production";
    const scriptSrc = isProd
      ? "script-src 'self' 'unsafe-inline'"
      : "script-src 'self' 'unsafe-inline' 'unsafe-eval'";
    const connectSrc = [
      "'self'",
      "https://api.groq.com",
      "https://res.cloudinary.com",
      "https://api.cloudinary.com",
      "https://api.cloud.llamaindex.ai",
    ].join(" ");

    const securityHeaders = [
      { key: "X-Frame-Options", value: "DENY" },
      { key: "X-Content-Type-Options", value: "nosniff" },
      { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
      {
        key: "Permissions-Policy",
        value: "camera=(), microphone=(), geolocation=()",
      },
      {
        key: "Content-Security-Policy",
        value: `default-src 'self'; ${scriptSrc}; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob: https://res.cloudinary.com; font-src 'self' data:; connect-src ${connectSrc}; frame-ancestors 'none'; base-uri 'self'; form-action 'self'`,
      },
    ];

    if (process.env.NODE_ENV === "production") {
      securityHeaders.push({
        key: "Strict-Transport-Security",
        value: "max-age=63072000; includeSubDomains; preload",
      });
    }

    return [
      {
        source: "/(.*)",
        headers: securityHeaders,
      },
    ];
  },
};

export default nextConfig;
