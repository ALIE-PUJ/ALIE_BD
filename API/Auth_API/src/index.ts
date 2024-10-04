import express from "express";
import type { CategoryDTO, LoginDTO, User } from "./model";
import { UserService } from "./services/UserService";
import swaggerUI from "swagger-ui-express";
import cors from "cors";

import { openAPISpecs } from "./configs/swagger";
import { generateToken } from "./configs/jwt";

const app = express()
const port = process.env.PORT || 2001;

// Configures /api/auth as the base path for the API
const router = express.Router();
app.use('/api/auth', router);

router.use(cors())
router.use(express.json());
router.use('/swagger', swaggerUI.serve, swaggerUI.setup(openAPISpecs));

router.post('/login', async (req, res) => {
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

router.put('/asignar_rol', async (req, res) => {
  const userCategory = req.body as CategoryDTO;

  try {
    await UserService.assignRole(userCategory.id_usuario, userCategory.id_categoria);

    res.status(200).json(true);
  } catch (error) {
    console.error("Error al asignar rol: " + error);

    res.status(400).json({ message: "Error al asignar rol" }); 
  }
})

app.listen(port, () => {
  console.log("Escuchando en el puerto " + port + "...");
});
