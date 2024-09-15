# Use the official Apache Flink image as the base image
FROM apache/flink:1.17.1

# Install Python and necessary packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install apache-flink

# # Install Kafka connector for Flink (ensure compatibility with Flink version)
# RUN wget https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka_2.12/1.15.2/flink-connector-kafka_2.12-1.15.2.jar \
#     -P /opt/flink/lib/

# Set up any Python packages you may need (e.g., Kafka Python clients)
RUN pip3 install kafka-python

# Optional: Set environment variables, if necessary
ENV FLINK_PYTHON_EXECUTABLE=python3

# Add entrypoint script to run the job (optional, if you need automated job execution)
CMD ["bash"]


docker compose exec jobmanager ./bin/flink run -py /flink_jobs/main.py -d