import express from 'express';
import { expressjwt, type Request as JWTRequest } from 'express-jwt';
import swaggerUI from 'swagger-ui-express';
import { openAPISpecs } from './configs/swagger';
import type { User } from './model';
import { UserService } from './services/UserService';
import cors from 'cors';


console.log("Inicializando express...");
const app = express();
const port = process.env.PORT || 2000;
const secret = process.env.SECRET || "superdupersecretsetanenvvarforprod";

app.use(cors());
app.use('/swagger', swaggerUI.serve, swaggerUI.setup(openAPISpecs));

/**
 * @swagger
 * /verify:
 *   post:
 *     summary: Verifica si el token es válido
 *     description: Verifica si el token en el header Authorization es válido
 *     produces:
 *       - application/json
 *     responses:
 *      200:
 *        description: Token válido
 *        schema:
 *        type: json
 */
app.post('/verify', expressjwt({
    secret: secret,
    algorithms: ["HS512"]
}), async (req: JWTRequest, res) => {
    console.log("Token válido");

    console.log("Buscando información del usuario");
    const usuarios = await UserService.findUser(req.auth.id_usuario);

    if (usuarios.length === 0) {
        console.log("Usuario no encontrado");
        return res.status(401).json({ error: "Usuario no encontrado" });
    } else {
        const user: User = usuarios[0];
        console.log("Usuario autenticado: " + user.usuario);
        return res.status(200).json(user);
    }
});

app.listen(port, () => {
    console.log("Escuchando en el puerto " + port + "...");
});
