FROM node:alpine

COPY package.json ./
COPY package-lock.json ./
COPY src ./src

RUN npm install

CMD [ "npm", "start" ]