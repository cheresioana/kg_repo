# Use an official Python runtime as a parent image
FROM python:3.8

COPY requirements.txt /

RUN /usr/local/bin/python -m pip install --upgrade pip && pip install -r /requirements.txt

# Set the working directory to /app
RUN mkdir /app
COPY model.proto client.py /app/

# Copy the current directory contents into the container at /app
COPY . /app
COPY model.proto /model.proto

# COPY license.json /license.json

# Install any needed packages specified in requirements.txt
#RUN pip install -r requirements.txt

WORKDIR /app

RUN python3 -m grpc_tools.protoc --python_out=. --proto_path=. --grpc_python_out=. *.proto

EXPOSE 8061
# Run the API application
CMD ["python", "client.py"]