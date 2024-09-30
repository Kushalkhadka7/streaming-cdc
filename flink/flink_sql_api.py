import logging
import sys

from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    env.add_jars("file:///../opt/flink/lib/flink-sql-connector-elasticsearch7-1.16.0.jar")

    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()

    table_env = StreamTableEnvironment.create(stream_execution_environment=env, environment_settings=settings)
    table_env.get_config().get_configuration().set_boolean("python.fn-execution.memory.managed", True)

    # Use default catalog and database
    table_env.use_catalog('default_catalog')
    table_env.use_database('default_database')

    table_env.execute_sql("""
        CREATE TABLE orders (
            payload ROW<
                after ROW<
                    id INT,
                    product_id STRING,
                    order_date TIMESTAMP(3),
                    order_status STRING,
                    order_total DECIMAL(10, 2),
                    order_quantity INT,
                    created_at TIMESTAMP(3),
                    updated_at TIMESTAMP(3)
                >
            >
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'orders.public.orders',
            'properties.bootstrap.servers' = 'broker1:29092',
            'properties.group.id' = 'flink_group',
            'format' = 'json',
            'json.fail-on-missing-field' = 'false',
            'json.ignore-parse-errors' = 'true',
            'scan.startup.mode' = 'earliest-offset'
        )
    """)

    table_env.execute_sql("""
        CREATE TABLE shipments (
            payload ROW<
                after ROW<
                    id INT,
                    order_id STRING,
                    tracking_number STRING,
                    shipment_date TIMESTAMP(3),
                    delivery_date TIMESTAMP(3),
                    shipment_status STRING,
                    shipping_mechanism STRING,
                    shipping_address STRING,
                    created_at TIMESTAMP(3),
                    updated_at TIMESTAMP(3)
                >
            >
         ) WITH (
            'connector' = 'kafka',
            'topic' = 'orders.public.shipments',
            'properties.bootstrap.servers' = 'broker1:29092',
            'properties.group.id' = 'flink_group1',
            'format' = 'json',
            'json.fail-on-missing-field' = 'false',
            'json.ignore-parse-errors' = 'true',
            'scan.startup.mode' = 'earliest-offset'
         )
     """)

    table_env.execute_sql("""
        CREATE TABLE products (
            payload ROW<
                after ROW<
                    id INT,
                    name STRING,
                    price FLOAT,
                    description TIMESTAMP(3),
                    quantity INT,
                    WARRENTY STRING,
                    created_at TIMESTAMP(3),
                    updated_at TIMESTAMP(3)
                >
            >
         ) WITH (
            'connector' = 'kafka',
            'topic' = 'dbo.products',
            'properties.bootstrap.servers' = 'broker1:29092',
            'properties.group.id' = 'products',
            'format' = 'json',
            'json.fail-on-missing-field' = 'false',
            'json.ignore-parse-errors' = 'true',
            'scan.startup.mode' = 'earliest-offset'
         )
     """)

    table_env.execute_sql("""
        CREATE TABLE elasticsearch_sink (
            order_id INT,
            product_id STRING,
            order_status STRING,
            shipping_address STRING,
            PRIMARY KEY (order_id) NOT ENFORCED
        ) WITH (
            'connector' = 'elasticsearch-7',
            'hosts' = 'http://elasticsearch:9200',
            'index' = 'orders_shipments',
            'sink.bulk-flush.interval' = '1000',
            'sink.bulk-flush.backoff.delay' = '1000',
            'format' = 'json',
            'document-id.key-delimiter' = '$',
            'sink.bulk-flush.max-size' = '42mb',
            'sink.bulk-flush.max-actions' = '32'
        )
    """)

    joinned_query = table_env.sql_query("""
        SELECT
            o.payload.after.id AS order_id,
            p.payload.after.id AS product_id,
            o.payload.after.order_status AS order_status,
            s.payload.after.shipping_address AS shipping_address,
        FROM orders o
        INNER JOIN products AS p
            ON CAST(p.payload.after.id AS STRING) = o.payload.after.product_id
        INNER JOIN shipments AS s
            ON CAST(o.payload.after.id AS STRING) = s.payload.after.order_id
    """)

    joinned_query.execute().print()

    env.execute("Kafka PyFlink Streaming Job")

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")

    main()
