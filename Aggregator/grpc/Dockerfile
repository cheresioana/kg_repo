# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /app
WORKDIR /aggregator

# Copy the current directory contents into the container at /app
COPY .. /aggregator

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8061

# Run the API application
CMD ["python", "client.py"]