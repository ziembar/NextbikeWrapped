FROM node:alpine

WORKDIR /usr/src/app/frontend

COPY frontend .

RUN npm install -g @angular/cli

RUN npm install

WORKDIR /usr/src/app/frontend/src
EXPOSE 5000

CMD ["ng", "serve", "--host", "0.0.0.0", "--disable-host-check"]