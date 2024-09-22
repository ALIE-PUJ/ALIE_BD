import bcrypt from "bcrypt";

import { client } from "../src/configs/postgres";
import type { User } from "../src/model";

// Usage: DB_HOST=localhost DB_USER=root DB_PASSWORD=pass DB_DB=alie_db bun run scripts/createUser.ts

const user: User = {
  id_usuario: "10",
  usuario: "Juan Camilo",
  email: "sanchezjcamilo@javeriana.edu.co",
  id_categoria: 1,
  contrasena: "123456"
}

if (user.contrasena) {
  await client.query("INSERT INTO usuario (id_usuario, usuario, email, id_categoria, contrasena) VALUES ($1, $2, $3, $4, $5) ON CONFLICT (id_usuario) DO NOTHING", [user.id_usuario, user.usuario, user.email, user.id_categoria, bcrypt.hashSync(user.contrasena, 10)]);
  console.log("Usuario creado exitosamente");
} else {
  console.error("No se puede crear un usuario sin contraseña");
}

await client.end();