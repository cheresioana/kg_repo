FROM ubuntu:20.04

# Set the working directory to /app
WORKDIR /app

COPY data_formats.proto /model.proto

# Install Python, pip, and necessary tools
RUN apt-get update && \
    apt-get install -y python3.8 python3-pip && \
    pip3 install --upgrade pip

# Install gRPC tools
RUN pip3 install grpcio-tools

# Copy the current directory contents into the container at /app
COPY . /app

# Run the protoc command
RUN python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. *.proto

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

RUN pip3 install plotly

# Expose ports
EXPOSE 8062 8061

# Run app.py when the container launches
CMD python3 grpcAPI/app.py