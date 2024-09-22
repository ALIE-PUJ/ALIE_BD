import { client } from "../configs/postgres";
import type { User } from "../model";
import bcrypt from "bcrypt";


export const UserService = {
  findUser: async (id_usuario: number) => {
    const result = await client.query("SELECT * FROM usuario u WHERE u.id_usuario = $1", [id_usuario]);
    return result.rows as User[];
  },
  findUserByEmail: async (email: string) => {
    const result = await client.query("SELECT * FROM usuario u WHERE u.email = $1", [email]);
    return result.rows[0] as User;
  },
  authenticate: async (email: string, password: string) => {
    const user = await UserService.findUserByEmail(email);
    const success = bcrypt.compareSync(password, user.contrasena);
    return {
      success,
      user: success ? user : null,
    };
  }
};
