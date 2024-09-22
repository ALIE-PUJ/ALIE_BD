import { client } from "../configs/postgres";
import type { User } from "../model";
import bcrypt from "bcrypt";


export const UserService = {
  findUser: async (id_usuario: number) => {
    const result = await client.query("SELECT * FROM usuario u WHERE u.id_usuario = $1", [id_usuario]);
    return result.rows as User[];
  },
  findUserByEmail: async (email: string) => {
    console.log("Buscando usuario con email: " + email);
    const result = await client.query("SELECT * FROM usuario u WHERE u.email = $1", [email]);

    // Verificar si retornó el usuario
    if (result.rowCount !== null) {
      console.log("Se encontraron " + result.rowCount + " usuarios");

      if (result.rowCount === 1) {
        console.log("Usuario encontrado: " + JSON.stringify(result.rows));
      } else if (result.rowCount > 1) {
        console.error("Se encontraron múltiples usuarios con el mismo email");
        return null;
      } else if (result.rowCount === 0) {
        console.error("No se encontró ningún usuario con el email: " + email);
        return null;
      }
    }

    console.log("Resultado: " + JSON.stringify(result.rows));
    return result.rows[0] as User;
  },
  authenticate: async (email: string, password: string) => {
    const user = await UserService.findUserByEmail(email);
    let success;
    if (user.contrasena) {
      success = bcrypt.compareSync(password, user.contrasena);
    } else {
      success = false;
    }
    return {
      success,
      user: success ? {
        ...user,
        contrasena: undefined,
      } : null,
    };
  }
};
