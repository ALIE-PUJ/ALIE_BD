export interface AuthRequest extends Express.Request {
  auth: {
    id_usuario: string;
    usuario: string;
    contrasena: string;
    email: string;
    id_categoria: number;
  }
}