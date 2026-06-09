import Link from "next/link";
import { auth } from "@/auth";
import { logout } from "@/app/actions/auth";

export default async function Header() {
  const session = await auth();
  const user = session?.user;

  return (
    <header className="sticky top-0 z-50 bg-[var(--brand)] text-white shadow-md">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6">
        <Link href="/" className="flex items-center gap-3">
          <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-white/15 text-lg font-bold">
            C
          </span>
          <span className="text-lg font-semibold tracking-tight">
            Ceil UFAS1
          </span>
        </Link>

        <nav className="flex items-center gap-1 text-sm font-medium">
          <Link
            href="/"
            className="rounded-md px-3 py-2 transition-colors hover:bg-white/15"
          >
            Accueil
          </Link>

          {user ? (
            <>
              <Link
                href="/dashboard"
                className="rounded-md px-3 py-2 transition-colors hover:bg-white/15"
              >
                Tableau de bord
              </Link>
              <span className="hidden px-2 text-white/80 sm:inline">
                {user.name ?? user.email}
              </span>
              <form action={logout}>
                <button
                  type="submit"
                  className="rounded-md bg-white/15 px-3 py-2 transition-colors hover:bg-white/25"
                >
                  Déconnexion
                </button>
              </form>
            </>
          ) : (
            <>
              <Link
                href="/login"
                className="rounded-md px-3 py-2 transition-colors hover:bg-white/15"
              >
                Connexion
              </Link>
              <Link
                href="/register"
                className="rounded-md bg-white px-3 py-2 font-semibold text-[var(--brand)] transition-colors hover:bg-white/90"
              >
                Inscription
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
