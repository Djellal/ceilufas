import Link from "next/link";
import { LoginForm } from "./login/login-form";

const courses = [
  { fr: "Anglais", ar: "اللغة الانجليزية" },
  { fr: "Français", ar: "اللغة الفرنسية" },
  { fr: "Espagnol", ar: "اللغة الاسبانية" },
  { fr: "Allemand", ar: "اللغة الالمانية" },
  { fr: "Turc", ar: "اللغة التركية" },
  { fr: "Russe", ar: "اللغة الروسية" },
  { fr: "Arabe", ar: "اللغة العربية" },
  { fr: "Italien", ar: "اللغة الايطالية" },
  { fr: "Chinois", ar: "اللغة الصينية" },
];

export default function Home() {
  return (
    <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
      {/* Hero + login */}
      <section className="grid gap-8 lg:grid-cols-[1.4fr_1fr]">
        <div className="rounded-xl bg-[var(--brand)] p-8 text-white shadow-sm">
          <p dir="rtl" className="text-right text-base leading-8">
            مركز التعليم المكثف للغات مصلحة من المصالح المشتركة التابعة للجامعة.
            يقدم المركز خدمة عمومية لتعليم اللغات موجهة بالدرجة الأولى لكافة أفراد
            الأسرة الجامعية من طلبة و أساتذة و موظفين إلا أنه مفتوح للخارجيين في
            إطار الاتفاقيات المبرمة مع مختلف القطاعات أو للأفراد الراغبين في تحسين
            مستواهم في اللغات.
          </p>
        </div>

        <div className="rounded-xl bg-white p-6 shadow-sm">
          <LoginForm />

          <div className="mt-6 border-t border-zinc-200 pt-4 text-center">
            <p className="text-sm text-zinc-600">
              Vous n&apos;avez pas encore de compte ?
            </p>
            <Link
              href="/register"
              className="mt-2 block w-full rounded-md border border-[var(--brand)] px-4 py-2 font-medium text-[var(--brand)] transition-colors hover:bg-[var(--brand)] hover:text-white"
            >
              Inscription
            </Link>
          </div>
        </div>
      </section>

      {/* Cours disponibles */}
      <section className="mt-12">
        <h2 className="mb-6 text-center text-2xl font-semibold text-zinc-800">
          Cours disponibles
        </h2>
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {courses.map((c) => (
            <article
              key={c.fr}
              className="flex flex-col overflow-hidden rounded-xl bg-white shadow-sm transition-shadow hover:shadow-md"
            >
              <div className="flex h-32 items-center justify-center bg-[var(--brand)]/10 text-4xl font-bold text-[var(--brand)]">
                {c.fr.charAt(0)}
              </div>
              <div className="flex flex-1 flex-col p-4">
                <h3 className="font-semibold text-zinc-800">{c.fr}</h3>
                <p dir="rtl" className="text-sm text-zinc-500">
                  {c.ar}
                </p>
                <div className="mt-4 flex gap-2">
                  <button className="flex-1 rounded-md bg-[var(--brand)] px-3 py-1.5 text-sm font-medium text-white transition-colors hover:bg-[var(--brand-hover)]">
                    Inscription
                  </button>
                  <button className="flex-1 rounded-md bg-emerald-600 px-3 py-1.5 text-sm font-medium text-white transition-colors hover:bg-emerald-700">
                    Réinscription
                  </button>
                </div>
              </div>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}
