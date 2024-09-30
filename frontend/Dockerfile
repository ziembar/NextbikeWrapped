# syntax = docker/dockerfile:1.2
FROM node:alpine as build

ARG API_URL

RUN echo $(echo API_URL)

WORKDIR /usr/src/app/frontend

COPY frontend .

RUN chmod +x /usr/src/app/frontend/startup.sh

RUN npm install -g @angular/cli

RUN npm install

RUN echo "${API_URL}" | /usr/src/app/frontend/startup.sh; exit 0
RUN --mount=type=secret,id=apiurl,dst=/etc/secrets/apiurl cat /etc/secrets/apiurl | /usr/src/app/frontend/startup.sh; exit 0


RUN ng build

FROM nginx:alpine

RUN rm /usr/share/nginx/html/index.html


COPY --from=build /usr/src/app/frontend/dist/frontend/browser /usr/share/nginx/html
COPY frontend/nginx.conf /etc/nginx/nginx.conf

EXPOSE 10000

# Start nginx
CMD ["nginx", "-g", "daemon off;"]