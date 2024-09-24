import logging
import sys

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.common import Types

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()

    table_env = StreamTableEnvironment.create(stream_execution_environment=env, environment_settings=settings)

    # kafka_sql_connector_jar = '../opt/flink/lib/flink-sql-connector-kafka-1.16.0.jar'
    #
    # print('----------------',kafka_sql_connector_jar)
    #
    # table_env.get_config().get_configuration().set_string('pipeline.jars','file://{}'.format(kafka_sql_connector_jar))

    # order_ddl = """
    #     CREATE TABLE orders (
    #         id INTEGER,
    #         product_id STRING,
    #         order_date TIMESTAMP(3),
    #         order_status STRING,
    #         order_quantity STRING,
    #         created_at TIMESTAMP(3),
    #         updated_at TIMESTAMP(3),
    #         watermark FOR `created_at` AS `created_at` - INTERVAL '5' SECOND
    #     ) WITH (
    #         'connector'='kafka',
    #         'topic'='orders.public.orders',
    #         'properties.bootstrap.servers' = 'broker1:29092',
    #         'properties.group.id' = 'product_id',
    #         'format' = 'json',
    #         'scan.startup.mode' = 'earliest-offset'
    #     )
    # """
    
    t_env.execute_sql("""
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
            >,
            WATERMARK FOR payload.after.created_at AS payload.after.created_at - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'orders.public.orders',
            'properties.bootstrap.servers' = 'broker1:29092',
            'properties.group.id' = 'flink_group',
            'format' = 'debezium-json',
            'scan.startup.mode' = 'earliest-offset'
        )
    """)

     # Query the created table to extract data from the nested structure
    result_table = t_env.sql_query("""
        SELECT 
            payload.after.id AS id, 
            payload.after.product_id AS product_id, 
            payload.after.order_status AS order_status, 
            payload.after.created_at AS created_at 
        FROM orders
    """)

    # Print the query results
    result_table.execute().print()

    # Step 6: Execute the environment
    env.execute("Kafka PyFlink Streaming Job")

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")

    main()



