# syntax = docker/dockerfile:1.2
FROM node:alpine as build

WORKDIR /usr/src/app/frontend

COPY frontend .

RUN chmod +x /usr/src/app/frontend/startup.sh

RUN npm install -g @angular/cli

RUN npm install

RUN --mount=type=secret,id=apiurl,dst=/etc/secrets/apiurl cat /etc/secrets/apiurl | /usr/src/app/frontend/startup.sh


RUN ng build

FROM nginx:alpine

RUN rm /usr/share/nginx/html/index.html


COPY --from=build /usr/src/app/frontend/dist/frontend/browser /usr/share/nginx/html

EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]