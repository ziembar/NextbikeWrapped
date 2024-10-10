# Use the official Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app/backend

COPY backend .

RUN pip install -r requirements.txt

EXPOSE 5000
WORKDIR /usr/src/app/backend/api
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
 
# CMD ["flask", "run", "--host=0.0.0.0"]
