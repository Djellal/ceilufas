"use client";

import { useActionState } from "react";
import { login, type FormState } from "@/app/actions/auth";

export function LoginForm() {
  const [state, formAction, pending] = useActionState<FormState, FormData>(
    login,
    undefined,
  );

  return (
    <form action={formAction} className="flex flex-col gap-4">
      {state?.error && (
        <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">
          {state.error}
        </p>
      )}
      <div>
        <label className="mb-1 block text-sm font-medium text-zinc-700">
          Email
        </label>
        <input
          name="email"
          type="email"
          required
          className="w-full rounded-md border border-zinc-300 px-3 py-2 outline-none focus:border-[var(--brand)] focus:ring-2 focus:ring-[var(--brand)]/20"
        />
        {state?.fieldErrors?.email && (
          <p className="mt-1 text-xs text-red-600">{state.fieldErrors.email[0]}</p>
        )}
      </div>
      <div>
        <label className="mb-1 block text-sm font-medium text-zinc-700">
          Mot de passe
        </label>
        <input
          name="password"
          type="password"
          required
          className="w-full rounded-md border border-zinc-300 px-3 py-2 outline-none focus:border-[var(--brand)] focus:ring-2 focus:ring-[var(--brand)]/20"
        />
        {state?.fieldErrors?.password && (
          <p className="mt-1 text-xs text-red-600">
            {state.fieldErrors.password[0]}
          </p>
        )}
      </div>
      <button
        type="submit"
        disabled={pending}
        className="rounded-md bg-[var(--brand)] px-4 py-2 font-medium text-white transition-colors hover:bg-[var(--brand-hover)] disabled:opacity-60"
      >
        {pending ? "Connexion…" : "Connexion"}
      </button>
    </form>
  );
}
