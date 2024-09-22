FROM node:alpine

COPY package.json ./
COPY package-lock.json ./
COPY src ./

RUN npm install

CMD [ "npm", "start" ]