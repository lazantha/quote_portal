# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install virtualenv
RUN pip install virtualenv

# Create a virtual environment
RUN virtualenv venv

# Activate the virtual environment and install dependencies
RUN /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir -r requirements.txt"

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Activate the virtual environment and run app.py
CMD ["/bin/bash", "-c", "source venv/bin/activate && python3 app.py"]
