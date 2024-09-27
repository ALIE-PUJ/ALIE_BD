import { client } from "../configs/postgres";
import type { User } from "../model";

async function findUser(id_usuario:number) {
  const result = await client.query("SELECT * FROM usuario u WHERE u.id_usuario = $1", [id_usuario]);
  return result.rows as User[];
}

export const UserService = {
  findUser
};
