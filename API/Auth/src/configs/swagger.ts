import swaggerJSDoc from "swagger-jsdoc";

const swagOpts: swaggerJSDoc.Options = {
  swaggerDefinition: {
    info: {
      title: "Auth Service API",
      version: "1.0.0",
      description: "API del servicio de autenticación"
    },
    security: [{ bearerAuth: [] }],
    securityDefinitions: {
      bearerAuth: {
        type: 'apiKey',
        name: 'Authorization',
        scheme: 'bearer',
        in: 'header',
      },
    },
  },
  apis: ["./index.ts", "./src/index.ts"],
};
const openAPISpecs = swaggerJSDoc(swagOpts);

export { openAPISpecs };