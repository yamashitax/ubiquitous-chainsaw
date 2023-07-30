# Use an official Python runtime as a parent image
FROM python:3.11.4-slim-bullseye

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run fetch.py when the container launches
CMD ["python", "fetch.py"]
