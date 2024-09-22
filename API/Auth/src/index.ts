import express from 'express';
import { expressjwt, type Request as JWTRequest } from 'express-jwt';
import { Client } from 'pg';
import swaggerJSDoc from 'swagger-jsdoc';
import swaggerUI from 'swagger-ui-express';
import { client } from './postgres';
import { openAPISpecs } from './swagger';
import type { AuthRequest } from './model';


console.log("Inicializando express...");
const app = express();
const port = process.env.PORT || 2000;
const secret = process.env.SECRET || "superdupersecretsetanenvvarforprod";

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
}), (req: JWTRequest, res) => {
    // client.query("SELECT * FROM usuario u WHERE u.id_usuario=$1::text", [req.auth.id_usuario]);

    res.status(200).json({ id_usuario: "Token válido" });
});

app.listen(port, () => {
    console.log("Escuchando en el puerto " + port + "...");
});
