export interface AuthRequest extends Express.Request {
  auth: User
}

export interface User {
  id_usuario: string;
  usuario: string;
  contrasena?: string;
  email: string;
  id_categoria: number;
}

export interface LoginDTO {
  email: string;
  contrasena: string;
}
