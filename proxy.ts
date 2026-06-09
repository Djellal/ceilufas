import NextAuth from "next-auth";
import { authConfig } from "./auth.config";

// Initialize Auth.js with only the edge-safe config (no Prisma adapter).
// The `authorized` callback in auth.config.ts decides access per route.
export const { auth: proxy } = NextAuth(authConfig);

export default proxy;

export const config = {
  // Run on app routes, excluding static assets and the auth API.
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico|.*\\.svg$).*)"],
};
