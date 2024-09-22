import swaggerJSDoc from "swagger-jsdoc";

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

export { openAPISpecs };