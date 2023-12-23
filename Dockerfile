# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run tests - Note: Usually, testing is handled outside of the Docker build process, often in a CI/CD pipeline
# We are not deploying so, we want our build process to fail if we have a new change with broken tests.
RUN pytest

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define the command to run the app using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
