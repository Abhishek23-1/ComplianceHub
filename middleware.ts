import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { AUTH_COOKIE_NAME, verifySessionToken } from "@/lib/auth-jwt";
import { verifyHealthBearer } from "@/lib/security/health-auth";

const PUBLIC_PATHS = [
  "/",
  "/login",
  "/api/auth/login",
  "/api/auth/logout",
  "/api/webhooks/agentmail",
  // Inngest serve endpoint — secured by INNGEST_SIGNING_KEY, not session cookies.
  // @see https://www.inngest.com/docs/learn/serving-inngest-functions
  "/api/inngest",
];

function isPublicPath(pathname: string): boolean {
  return (
    PUBLIC_PATHS.some(
      (path) => pathname === path || pathname.startsWith(`${path}/`)
    ) ||
    pathname.startsWith("/_next") ||
    pathname.startsWith("/favicon")
  );
}

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  try {
    if (isPublicPath(pathname)) {
      const response = NextResponse.next();
      response.headers.set("x-pathname", pathname);
      return response;
    }

    if (pathname.startsWith("/api/health")) {
      if (verifyHealthBearer(request.headers.get("authorization"))) {
        const response = NextResponse.next();
        response.headers.set("x-pathname", pathname);
        return response;
      }
    }

    const token = request.cookies.get(AUTH_COOKIE_NAME)?.value;
    const session = token ? await verifySessionToken(token) : null;

    if (!session) {
      if (pathname.startsWith("/api/")) {
        return NextResponse.json(
          { success: false, error: "Unauthorized" },
          { status: 401 }
        );
      }

      const loginUrl = new URL("/login", request.url);
      return NextResponse.redirect(loginUrl);
    }

    if (pathname === "/login") {
      return NextResponse.redirect(new URL("/dashboard", request.url));
    }

    const response = NextResponse.next();
    response.headers.set("x-pathname", pathname);
    return response;
  } catch (error) {
    console.error("[middleware] unhandled error:", error);

    if (pathname.startsWith("/api/")) {
      return NextResponse.json(
        { success: false, error: "Service unavailable" },
        { status: 503 }
      );
    }

    if (isPublicPath(pathname)) {
      return NextResponse.next();
    }

    return NextResponse.redirect(new URL("/login", request.url));
  }
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
