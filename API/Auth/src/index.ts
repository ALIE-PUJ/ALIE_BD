import express from 'express';
import { expressjwt } from 'express-jwt';
import { Client } from 'pg';


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
    })

app.post('/verify', expressjwt({
    secret: secret,
    algorithms: ["RS512"]
}),(_req, _res) => {
    client.query("SELECT * FROM ", []

    )
});

app.listen(port, () => {
    console.log("Escuchando en el puerto " + port + "...");
});
