FROM node:alpine as build

WORKDIR /usr/src/app/frontend

COPY frontend .

RUN npm install -g @angular/cli

RUN npm install

# Build the Angular project
RUN ng build

# Stage 2: Serve the Angular application with nginx
FROM nginx:alpine

# Copy the built Angular files from the previous stage
COPY --from=build /usr/src/app/frontend/dist /usr/share/nginx/html

# Copy custom nginx configuration if needed
# COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80 to the outside world
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]