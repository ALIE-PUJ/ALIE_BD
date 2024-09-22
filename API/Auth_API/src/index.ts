import express from "express";
import type { LoginDTO, User } from "./model";
import { UserService } from "./services/UserService";
import swaggerUI from "swagger-ui-express";
import { openAPISpecs } from "./configs/swagger";
import { generateToken } from "./configs/jwt";

const app = express()
const port = process.env.PORT || 2001;

app.use(express.json());
app.use('/swagger', swaggerUI.serve, swaggerUI.setup(openAPISpecs));

app.post('/login', async (req, res) => {
  const login_info = req.body as LoginDTO;

  let result = await UserService.authenticate(login_info.email, login_info.contrasena);

  if (result.success) {
    console.log("Usuario autenticado: " + result.user?.usuario);
    res.status(200).json({
      user: result.user,
      token: generateToken(result.user),
    });
  } else {
    res.status(401).json({ message: "Credenciales inválidas" });
  }
});

app.listen(port, () => {
  console.log("Escuchando en el puerto " + port + "...");
});
