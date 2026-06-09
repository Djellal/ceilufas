import type { NextAuthConfig } from "next-auth";
import type { Role } from "./generated/prisma/enums";

/**
 * Edge-safe Auth.js configuration shared between the proxy (middleware) and
 * the full server config in `auth.ts`. It must NOT import the Prisma adapter
 * or anything that relies on Node-only APIs.
 */
export const authConfig = {
  // Required for self-hosting (non-Vercel) so Auth.js trusts the request host.
  trustHost: true,
  pages: {
    signIn: "/login",
  },
  session: { strategy: "jwt" },
  providers: [],
  callbacks: {
    // Persist id + role into the JWT on sign in.
    jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.role = user.role;
      }
      return token;
    },
    // Expose id + role on the session object.
    session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string;
        session.user.role = token.role as Role;
      }
      return session;
    },
    // Route protection used by the proxy.
    authorized({ auth, request: { nextUrl } }) {
      const isLoggedIn = !!auth?.user;
      const role = auth?.user?.role;
      const { pathname } = nextUrl;

      // Protected areas
      const isDashboard = pathname.startsWith("/dashboard");
      const isAdmin = pathname.startsWith("/admin");
      const isTeacher = pathname.startsWith("/teacher");

      if (isAdmin) return isLoggedIn && role === "ADMIN";
      if (isTeacher) return isLoggedIn && (role === "TEACHER" || role === "ADMIN");
      if (isDashboard) return isLoggedIn;

      return true;
    },
  },
} satisfies NextAuthConfig;
