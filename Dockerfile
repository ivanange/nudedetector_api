# Use an official Python runtime as a parent image
FROM python:3.12-slim

RUN mkdir /app && chmod -R 777 /app

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the app will run on
EXPOSE 4000

# Run the command to start the app when the container launches
CMD ["gunicorn", "app:app", "--workers", "2", "--bind", "0.0.0.0:4000", "--log-file", "/app/nudedetector.log", "--log-level", "info"]
