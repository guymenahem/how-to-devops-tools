FROM node:14

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY client.js ./

COPY buying_intent.proto ./

CMD ["node", "client.js"]
