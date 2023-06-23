# Use an official Python runtime as a parent image
FROM python:3.11.3-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
#COPY ./logs ./logs
COPY ./users ./users
COPY ./config.py ./config.py
COPY ./database.py ./database.py
COPY ./.env ./.env
COPY ./main.py ./main.py


# Expose the port that the app will run on
EXPOSE 8000

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
