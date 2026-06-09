import Link from "next/link";
import { redirect } from "next/navigation";
import { auth } from "@/auth";

const roleLabels: Record<string, string> = {
  ADMIN: "Administrateur",
  TEACHER: "Enseignant",
  STUDENT: "Étudiant",
};

export default async function DashboardPage() {
  const session = await auth();
  if (!session?.user) redirect("/login");

  const role = session.user.role;

  return (
    <div className="mx-auto max-w-4xl px-4 py-12 sm:px-6">
      <h1 className="text-2xl font-semibold text-zinc-800">
        Bonjour, {session.user.name ?? session.user.email}
      </h1>
      <p className="mt-2 text-zinc-600">
        Vous êtes connecté en tant que{" "}
        <span className="font-medium text-[var(--brand)]">
          {roleLabels[role] ?? role}
        </span>
        .
      </p>

      <div className="mt-8 grid gap-4 sm:grid-cols-2">
        <section className="rounded-xl bg-white p-6 shadow-sm">
          <h2 className="font-semibold text-zinc-800">Espace étudiant</h2>
          <p className="mt-1 text-sm text-zinc-600">
            Consultez vos cours et vos inscriptions.
          </p>
        </section>

        {(role === "TEACHER" || role === "ADMIN") && (
          <Link
            href="/teacher"
            className="rounded-xl bg-white p-6 shadow-sm transition-shadow hover:shadow-md"
          >
            <h2 className="font-semibold text-zinc-800">Espace enseignant</h2>
            <p className="mt-1 text-sm text-zinc-600">
              Gérez vos classes et vos évaluations.
            </p>
          </Link>
        )}

        {role === "ADMIN" && (
          <Link
            href="/admin"
            className="rounded-xl bg-white p-6 shadow-sm transition-shadow hover:shadow-md"
          >
            <h2 className="font-semibold text-zinc-800">Administration</h2>
            <p className="mt-1 text-sm text-zinc-600">
              Gérez les utilisateurs, les rôles et les cours.
            </p>
          </Link>
        )}
      </div>
    </div>
  );
}
