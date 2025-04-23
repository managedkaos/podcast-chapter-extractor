# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV WORKDIR=/data
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR ${WORKDIR}
RUN mkdir -p ${WORKDIR}

# Install runtime dependencies
COPY requirements.txt /opt/
RUN pip install --no-cache-dir -r /opt/requirements.txt

# Copy and install the application
COPY script.py /usr/local/bin/
RUN chmod +x /usr/local/bin/script.py

# Run the script when the container launches
ENTRYPOINT ["/usr/local/bin/script.py"]
