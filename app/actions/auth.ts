"use server";

import { z } from "zod";
import bcrypt from "bcryptjs";
import { AuthError } from "next-auth";
import { prisma } from "@/lib/prisma";
import { signIn, signOut } from "@/auth";

export async function logout() {
  await signOut({ redirectTo: "/" });
}

export type FormState = {
  error?: string;
  fieldErrors?: Record<string, string[]>;
} | undefined;

const RegisterSchema = z.object({
  name: z.string().min(2, "Le nom doit contenir au moins 2 caractères.").trim(),
  email: z.string().email("Adresse e-mail invalide.").trim(),
  password: z
    .string()
    .min(8, "Le mot de passe doit contenir au moins 8 caractères."),
});

export async function register(
  _prevState: FormState,
  formData: FormData,
): Promise<FormState> {
  const parsed = RegisterSchema.safeParse({
    name: formData.get("name"),
    email: formData.get("email"),
    password: formData.get("password"),
  });

  if (!parsed.success) {
    return { fieldErrors: parsed.error.flatten().fieldErrors };
  }

  const { name, email, password } = parsed.data;
  const normalizedEmail = email.toLowerCase();

  const existing = await prisma.user.findUnique({
    where: { email: normalizedEmail },
  });
  if (existing) {
    return { error: "Un compte existe déjà avec cette adresse e-mail." };
  }

  const hashed = await bcrypt.hash(password, 10);
  await prisma.user.create({
    data: {
      name,
      email: normalizedEmail,
      password: hashed,
      // New users are students by default (schema default), set explicitly for clarity.
      role: "STUDENT",
    },
  });

  // Automatically sign the new user in and redirect to the dashboard.
  await signIn("credentials", {
    email: normalizedEmail,
    password,
    redirectTo: "/dashboard",
  });
}

const LoginSchema = z.object({
  email: z.string().email("Adresse e-mail invalide.").trim(),
  password: z.string().min(1, "Mot de passe requis."),
});

export async function login(
  _prevState: FormState,
  formData: FormData,
): Promise<FormState> {
  const parsed = LoginSchema.safeParse({
    email: formData.get("email"),
    password: formData.get("password"),
  });

  if (!parsed.success) {
    return { fieldErrors: parsed.error.flatten().fieldErrors };
  }

  try {
    await signIn("credentials", {
      email: parsed.data.email.toLowerCase(),
      password: parsed.data.password,
      redirectTo: "/dashboard",
    });
  } catch (error) {
    // AuthError = bad credentials; the success redirect is a different error
    // (NEXT_REDIRECT) that must be re-thrown to let Next.js perform the redirect.
    if (error instanceof AuthError) {
      return { error: "Identifiants incorrects. Veuillez réessayer." };
    }
    throw error;
  }
}
