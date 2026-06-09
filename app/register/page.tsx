import Link from "next/link";
import { RegisterForm } from "./register-form";

export default function RegisterPage() {
  return (
    <div className="mx-auto flex max-w-md flex-col px-4 py-16 sm:px-6">
      <h1 className="mb-6 text-center text-2xl font-semibold text-zinc-800">
        Inscription
      </h1>
      <div className="rounded-xl bg-white p-6 shadow-sm">
        <RegisterForm />
      </div>
      <p className="mt-6 text-center text-sm text-zinc-600">
        Vous avez déjà un compte ?{" "}
        <Link href="/login" className="font-medium text-[var(--brand)] hover:underline">
          Connexion
        </Link>
      </p>
    </div>
  );
}
