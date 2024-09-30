# Change Data Capture (CDC)

Change data capture for postgres and mssql database using debezium and streaming data processing.

Change Data Capture (CDC) is a technique used to identify and track changes made to data within a database. It provides a mechanism to capture only the modified data, rather than the entire dataset, resulting in significant efficiency gains and reduced data transfer volumes.

## Workflow diagram

![Architecture Diagram](./assets/finaldoc.png)

## Benefits

- Incremental Updates
- Real-time Processing
- Reduced Data Transfer
- Audit and Logging
- Event-Driven Architecture:

## Tools Used

- [PostgreSQL](https://www.postgresql.org/)
- [Mssql](https://www.microsoft.com/en-us/sql-server/sql-server-downloads)
- [Debezium](https://debezium.io/)
- [Apache Kafka](https://kafka.apache.org/)
- [Apache flink](https://flink.apache.org/)

## Background

Whenever any services writes data to any of the `CDC` enabled tables on these databases `(postgres or msslq)`, the CDC framework debezium picks up the changes and stream the CDC data to kafka stream respective topics. When we enable CDC with debezium it will automatically creates topic per table and the CDC is streamed to respective topic.

We have flink cluster, which reads the data from the respective kafka streams and do processing with the data. Once the processing is completed for the data, it either send the data to another kafka stream or dum to elasticsearch sink. Flink have many sinks supported.

## Requirements

| Name           | Version |
| -------------- | ------- |
| docker         | >= 20   |
| docker-compose | >= 2    |
| virtualenv     | >= 20   |

## Getting started

> **_NOTE:_** These steps should be followed in order.

- Use docker compose command to start mssql and postgres databases.
- Once the databases are up, test tables orders,shipments in postgres and products in mssql are automatically created.
- Use docker compose to start the kafka cluster, once the kafka cluster is ready use docker compose to up and start `debezium` cluster.
- At the same time start kafka control center and schema registry of kafka.
- When the debezium cluster is ready we need to start the data producers.
- Use docker compose to start load_products first and once it is completed start load_orders. The orders producer will auto generate fake order and shipment every 10 seconds and store it in the postgres database tables orders and shipments respectively.
- Start the flink cluster, it can be done using the docker compose as well. At the same time star the elastic search cluster also.
- Docker exec the flink jobmanger container.
- Navigate to /flink_jobs dir.
- Run `flink run -py main.py -d` command to submit the flink job.

## Dashboards

- Debezium [http://localhost:8081]
- Kafka Control Center [http://localhost:9021]
- Flink [http://localhost:8086]
