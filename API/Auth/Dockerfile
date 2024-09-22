FROM node:alpine

COPY package.json ./
COPY bun.lockb ./
COPY src ./

RUN npm install

CMD [ "npm", "start" ]