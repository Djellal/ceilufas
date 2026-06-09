const socials = [
  {
    label: "Facebook",
    href: "#",
    path: "M22 12.06C22 6.5 17.52 2 12 2S2 6.5 2 12.06c0 5 3.66 9.15 8.44 9.94v-7.03H7.9v-2.9h2.54V9.84c0-2.52 1.49-3.92 3.78-3.92 1.1 0 2.24.2 2.24.2v2.47h-1.26c-1.24 0-1.63.78-1.63 1.57v1.89h2.78l-.44 2.9h-2.34V22c4.78-.79 8.43-4.94 8.43-9.94Z",
  },
  {
    label: "Instagram",
    href: "#",
    path: "M12 2c2.72 0 3.06.01 4.12.06 1.07.05 1.79.22 2.43.47.66.25 1.22.6 1.77 1.15.55.55.9 1.11 1.15 1.77.25.64.42 1.36.47 2.43.05 1.06.06 1.4.06 4.12s-.01 3.06-.06 4.12c-.05 1.07-.22 1.79-.47 2.43-.25.66-.6 1.22-1.15 1.77-.55.55-1.11.9-1.77 1.15-.64.25-1.36.42-2.43.47-1.06.05-1.4.06-4.12.06s-3.06-.01-4.12-.06c-1.07-.05-1.79-.22-2.43-.47a4.9 4.9 0 0 1-1.77-1.15 4.9 4.9 0 0 1-1.15-1.77c-.25-.64-.42-1.36-.47-2.43C2.01 15.06 2 14.72 2 12s.01-3.06.06-4.12c.05-1.07.22-1.79.47-2.43.25-.66.6-1.22 1.15-1.77.55-.55 1.11-.9 1.77-1.15.64-.25 1.36-.42 2.43-.47C8.94 2.01 9.28 2 12 2Zm0 5a5 5 0 1 0 0 10 5 5 0 0 0 0-10Zm0 8.25a3.25 3.25 0 1 1 0-6.5 3.25 3.25 0 0 1 0 6.5ZM17.5 6.75a1.25 1.25 0 1 0 0-2.5 1.25 1.25 0 0 0 0 2.5Z",
  },
  {
    label: "LinkedIn",
    href: "#",
    path: "M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14ZM8.34 18.34v-8H5.67v8h2.67ZM7 9.13a1.55 1.55 0 1 0 0-3.1 1.55 1.55 0 0 0 0 3.1Zm11.34 9.21v-4.39c0-2.35-1.25-3.44-2.93-3.44-1.35 0-1.96.74-2.3 1.27v-1.09h-2.67v8h2.67v-4.43c0-.23.02-.47.09-.64.18-.47.61-.95 1.33-.95.94 0 1.32.72 1.32 1.77v4.25h2.67Z",
  },
  {
    label: "X",
    href: "#",
    path: "M18.9 2H22l-7.1 8.12L23 22h-6.4l-5-6.55L5.8 22H2.7l7.6-8.69L2 2h6.56l4.52 5.98L18.9 2Zm-1.12 18.06h1.7L7.3 3.85H5.5l12.28 16.2Z",
  },
  {
    label: "YouTube",
    href: "#",
    path: "M23 12s0-3.2-.41-4.74a2.5 2.5 0 0 0-1.76-1.77C19.28 5.07 12 5.07 12 5.07s-7.28 0-8.83.42a2.5 2.5 0 0 0-1.76 1.77C1 8.8 1 12 1 12s0 3.2.41 4.74a2.5 2.5 0 0 0 1.76 1.77c1.55.42 8.83.42 8.83.42s7.28 0 8.83-.42a2.5 2.5 0 0 0 1.76-1.77C23 15.2 23 12 23 12Zm-13 3.27V8.73L15.5 12 10 15.27Z",
  },
];

export default function Footer() {
  return (
    <footer className="bg-[var(--brand)] text-white">
      <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
        <div className="grid gap-8 sm:grid-cols-2">
          <div>
            <h3 className="text-lg font-semibold">CEIL UFAS1</h3>
            <p className="mt-1 text-sm text-white/80">Université Sétif -1-</p>
          </div>

          <ul className="space-y-2 text-sm text-white/90">
            <li className="flex items-start gap-2">
              <span aria-hidden>📍</span>
              <span>
                Campus El Bez, Ex-Faculté de Droit (Actuellement Département
                d&apos;Agronomie)
              </span>
            </li>
            <li className="flex items-center gap-2">
              <span aria-hidden>📞</span>
              <a href="tel:+21336620996" className="hover:underline">
                (+213) 036.62.09.96
              </a>
            </li>
            <li className="flex items-center gap-2">
              <span aria-hidden>✉️</span>
              <a href="mailto:ceil@univ-setif.dz" className="hover:underline">
                ceil@univ-setif.dz
              </a>
            </li>
            <li className="flex items-center gap-2">
              <span aria-hidden>🌐</span>
              <a
                href="https://ceil.univ-setif.dz"
                target="_blank"
                rel="noopener noreferrer"
                className="hover:underline"
              >
                https://ceil.univ-setif.dz
              </a>
            </li>
          </ul>
        </div>

        <div className="mt-8 flex justify-center gap-4">
          {socials.map((s) => (
            <a
              key={s.label}
              href={s.href}
              aria-label={s.label}
              className="flex h-10 w-10 items-center justify-center rounded-full bg-white/15 transition-colors hover:bg-white/25"
            >
              <svg
                viewBox="0 0 24 24"
                className="h-5 w-5 fill-current"
                aria-hidden
              >
                <path d={s.path} />
              </svg>
            </a>
          ))}
        </div>

        <p className="mt-8 border-t border-white/20 pt-6 text-center text-xs text-white/70">
          Ceilapp v1.0.0 — Tous droits réservés Ⓒ 2025
        </p>
      </div>
    </footer>
  );
}
