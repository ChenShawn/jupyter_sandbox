# Base image
FROM pytorch/pytorch:2.9.1-cuda12.6-cudnn9-runtime

# Set non-interactive mode for apt
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
RUN mkdir -p /workspace
WORKDIR /workspace

# Copy requirements.txt and install Python dependencies
COPY ./jupyter_sandbox/requirements.txt /workspace/requirements.txt
RUN pip install -r /workspace/requirements.txt

# Copy jupyter_sandbox folder
COPY ./jupyter_sandbox /workspace/jupyter_sandbox

# Install build tools for Redis compilation
RUN apt-get update && apt-get install -y build-essential tcl

# Copy Redis tar.gz and install
COPY ./redis/8.0.2.tar.gz /workspace/8.0.2.tar.gz
RUN tar -xzf /workspace/8.0.2.tar.gz -C /workspace && \
    cd /workspace/redis-8.0.2 && \
    make && make install && make test

# Expose ports 18901 to 18916
EXPOSE 18901-18916

# Set default working directory for container
WORKDIR /workspace/jupyter_sandbox

# Set default command
CMD ["bash", "./start_serving.sh"]

