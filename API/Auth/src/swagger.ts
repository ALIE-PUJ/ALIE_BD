import swaggerJSDoc from "swagger-jsdoc";

const swagOpts: swaggerJSDoc.Options = {
  swaggerDefinition: {
    info: {
      title: "Auth API",
      version: "1.0.0",
      description: "API de autenticación"
    },
    security: [{ bearerAuth: [] }],
    securityDefinitions: {
      bearerAuth: {
        type: 'apiKey',
        name: 'x-auth-token',
        scheme: 'bearer',
        in: 'header',
      },
    },
  },
  apis: ["./src/index.ts"],
};
const openAPISpecs = swaggerJSDoc(swagOpts);

export { openAPISpecs };