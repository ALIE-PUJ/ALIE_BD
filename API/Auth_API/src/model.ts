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

/**
 * @swagger
 * components:
 *  schemas:
 *   LoginDTO:
 *    type: object
 *    required:
 *     - email
 *     - contrasena
 *    properties:
 *     email:
 *      type: string
 *     contrasena:
 *      type: string
 *   User:
 *    type: object
 *    required:
 *     - id_usuario
 *     - usuario
 *     - email
 *     - id_categoria
 *    properties:
 *     id_usuario:
 *      type: number
 *     usuario:
 *      type: string
 *     email:
 *      type: string
 *     id_categoria:
 *      type: number
 */
