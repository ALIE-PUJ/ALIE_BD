import express from "express";
import type { LoginDTO, User } from "../model";
import { UserService } from "../services/UserService";
import swaggerUI from "swagger-ui-express";
import { openAPISpecs } from "../configs/swagger";

const app = express()
const port = process.env.PORT || 2001;

app.use(express.json());
app.use('/swagger', swaggerUI.serve, swaggerUI.setup(openAPISpecs));

/**
 * @swagger
 * /login:
 *  post:
 *   description: Autenticar un usuario
 *   requestBody:
 *    required: true
 *   content:
 *    application/json:
 *     schema:
 *      $ref: '#/components/schemas/LoginDTO'
 *   responses:
 *    200:
 *     description: Usuario autenticado
 *     content:
 *      application/json:
 *       schema:
 *        $ref: '#/components/schemas/User'
 *    401:
 *     description: Credenciales inválidas
 *     content:
 *      application/json:
 */
app.post('/login', async (req, res) => {
  const login_info = req.body as LoginDTO;

  let result = await UserService.authenticate(login_info.email, login_info.contrasena);

  if (result.success) {
    console.log("Usuario autenticado: " + result.user?.usuario);
    res.status(200).json(result.user);
  } else {
    res.status(401).json({ message: "Credenciales inválidas" });
  }
});

app.listen(port, () => {
  console.log("Escuchando en el puerto " + port + "...");
});
