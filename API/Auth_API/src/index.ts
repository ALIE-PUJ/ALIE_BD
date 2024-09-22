import express from "express";

const app = express()
const port = process.env.PORT || 2001;

app.use(express.json());

app.post('/login', (_req, _res) => {

});

app.listen(port, () => {
    console.log("Escuchando en el puerto " + port + "...");
});
