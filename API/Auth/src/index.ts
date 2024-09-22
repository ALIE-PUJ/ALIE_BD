import express from 'express';
import { expressjwt } from 'express-jwt';
import { Client } from 'pg';
import swaggerJSDoc from 'swagger-jsdoc';
import swaggerUI from 'swagger-ui-express';


console.log("Inicializando express...");
const app = express();
const port = process.env.PORT || 2000;
const secret = process.env.SECRET || "superdupersecretsetanenvvarforprod";
const client = new Client({
    user: process.env.DB_USER || "root",
    password: process.env.DB_PASSWORD || "password",
    host: process.env.DB_HOST || "host",
    port: +process.env.DB_PORT || 5432,
    database: process.env.DB_DB || "prueba"
});

client.connect()
    .then(() => {
        console.log("Connected to PostgreSQL database")
    })
    .catch((e) => {
        console.error("Error connecting to PostgreSQL database", e)
    });

const swagOpts: swaggerJSDoc.Options = {
    definition: {
        info: {
            title: "Auth API",
            version: "1.0.0",
            description: "API de autenticación"
        },
    },
    apis: ["./src/index.ts"],
    authAction: {
        JWT: {
            name: "JWT",
            schema: {
                type: "apiKey",
                in: "header",
                name: "Authorization",
                description: ""
            },
            value: "Bearer <JWT>"
        }
    }
};
const openAPISpecs = swaggerJSDoc(swagOpts);

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
    algorithms: ["RS512"]
}),(_req, _res) => {
    client.query("SELECT * FROM usuario u WHERE u.id_usuario=$1::text", [])
});

app.listen(port, () => {
    console.log("Escuchando en el puerto " + port + "...");
});
