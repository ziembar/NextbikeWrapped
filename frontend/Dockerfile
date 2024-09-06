FROM node:alpine

WORKDIR /usr/src/app/frontend

COPY frontend .

RUN chmod +x /usr/src/app/frontend/startup.sh

RUN npm install -g @angular/cli

RUN npm install

WORKDIR /usr/src/app/frontend/src
EXPOSE 5000


ENTRYPOINT ["/usr/src/app/frontend/startup.sh"]
CMD ["ng", "serve", "--host", "0.0.0.0", "--disable-host-check"]