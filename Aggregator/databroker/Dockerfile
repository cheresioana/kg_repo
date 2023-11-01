FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app
COPY data_formats.proto /model.proto

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
RUN pip3 install grpcio-tools
RUN python3 -m grpc_tools.protoc --python_out=. --proto_path=. --grpc_python_out=. *.proto

EXPOSE 8061

# Run the API application
CMD ["python", "server.py"]