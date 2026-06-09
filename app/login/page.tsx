import Link from "next/link";
import { LoginForm } from "./login-form";

export default function LoginPage() {
  return (
    <div className="mx-auto flex max-w-md flex-col px-4 py-16 sm:px-6">
      <h1 className="mb-6 text-center text-2xl font-semibold text-zinc-800">
        Connexion
      </h1>
      <div className="rounded-xl bg-white p-6 shadow-sm">
        <LoginForm />
      </div>
      <p className="mt-6 text-center text-sm text-zinc-600">
        Vous n&apos;avez pas encore de compte ?{" "}
        <Link href="/register" className="font-medium text-[var(--brand)] hover:underline">
          Inscription
        </Link>
      </p>
    </div>
  );
}
