import { Client } from "pg";

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

export { client };