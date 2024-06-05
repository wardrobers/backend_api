# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container to the root of the project
WORKDIR /backend_api

# Copy the current directory contents into the container at /backend_api
COPY . /backend_api

RUN apt-get update && apt-get install -y python3-opencv
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
EXPOSE 5432

# Define environment variable
ENV PORT 8080

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]