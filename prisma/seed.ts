import "dotenv/config";
import bcrypt from "bcryptjs";
import { prisma } from "../lib/prisma";

async function main() {
  const accounts = [
    { name: "Administrateur", email: "admin@ceil.univ-setif.dz", password: "admin1234", role: "ADMIN" as const },
    { name: "Enseignant", email: "teacher@ceil.univ-setif.dz", password: "teacher1234", role: "TEACHER" as const },
  ];

  for (const a of accounts) {
    const password = await bcrypt.hash(a.password, 10);
    await prisma.user.upsert({
      where: { email: a.email },
      update: { role: a.role },
      create: { name: a.name, email: a.email, password, role: a.role },
    });
    console.log(`Seeded ${a.role}: ${a.email} (password: ${a.password})`);
  }
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(() => prisma.$disconnect());
