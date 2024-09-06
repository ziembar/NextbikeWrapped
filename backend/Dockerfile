# Use the official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app/backend

COPY backend .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
WORKDIR /usr/src/app/backend/api
 
CMD ["flask", "run", "--host=0.0.0.0"]
