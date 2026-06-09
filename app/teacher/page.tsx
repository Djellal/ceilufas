import { redirect } from "next/navigation";
import { auth } from "@/auth";

export default async function TeacherPage() {
  const session = await auth();
  const role = session?.user?.role;
  if (role !== "TEACHER" && role !== "ADMIN") redirect("/dashboard");

  return (
    <div className="mx-auto max-w-4xl px-4 py-12 sm:px-6">
      <h1 className="text-2xl font-semibold text-zinc-800">Espace enseignant</h1>
      <p className="mt-2 text-zinc-600">
        Gérez vos classes, vos cours et les évaluations de vos étudiants.
      </p>
    </div>
  );
}
