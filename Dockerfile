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

RUN apt-get update && apt-get install -y curl

RUN curl -o /app/features/dataset_reduced.csv_HOG_.rbf -L "https://www.dropbox.com/scl/fi/jlq2vhnnfcizja8ptmstx/dataset_reduced.csv_HOG_.rbf?rlkey=g4ntgfki040nqyr709lt5bnti&st=dgdbqfep&dl=1"

RUN curl -o /app/models/hog_mixture_ratio_0_01-03-2023 11-01-11_model.sav -L "https://www.dropbox.com/scl/fi/xfw1z9fgzdumevafihq75/hog_mixture_ratio_0_01-03-2023-11-01-11_model.sav?rlkey=6w3jlplmxgmuroyozzquubv9z&st=8rrgfxgq&dl=1"

# Expose the port the app will run on
EXPOSE 5000

# Run the command to start the app when the container launches
CMD ["gunicorn", "app:app", "--workers", "2", "--bind", "0.0.0.0:5000", "--log-file", "/app/nudedetector.log", "--log-level", "info"]
