export interface AuthRequest extends Express.Request {
  auth: User
}

export interface User {
  id_usuario: number;
  usuario: string;
  contrasena?: string;
  email: string;
  id_categoria: number;
}

export interface LoginDTO {
  email: string;
  contrasena: string;
}

export interface CategoryDTO {
  id_categoria: number;
  id_usuario: number;
}