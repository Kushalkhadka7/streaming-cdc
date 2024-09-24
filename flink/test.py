from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.watermark_strategy import WatermarkStrategy

# from pyflink.datastream.functions import KeySelector
# from pyflink.datastream.window import TumblingEventTimeWindows
# from pyflink.common.time import Time

from pyflink.datastream import CoProcessFunction 
from pyflink.datastream.state import ValueStateDescriptor
from pyflink.common import Types

import json

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    # Create Kafka source with no specific schema, using SimpleStringSchema to capture raw messages
    orders_source = KafkaSource.builder() \
        .set_bootstrap_servers("broker1:29092") \
        .set_topics("orders.public.orders") \
        .set_group_id("product_id") \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .build()

    shipments_source = KafkaSource.builder() \
        .set_bootstrap_servers("broker1:29092") \
        .set_topics("orders.public.shipments") \
        .set_group_id("order_id") \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .build()

    # Create a DataStream for the raw Kafka messages
    orders_stream = env.from_source(
        orders_source,
        WatermarkStrategy.no_watermarks(),
        "orders_source"
    )

    # Create a DataStream for the raw Kafka messages
    shipments_stream= env.from_source(
        shipments_source,
        WatermarkStrategy.no_watermarks(),
        "shipments_source"
    )

    class JoinStreams(CoProcessFunction):
        def __init__(self):
            self.orders_state = ValueStateDescriptor("orders_state", Types.PICKLED_BYTE_ARRAY())
            self.shipments_state = ValueStateDescriptor("shipments_state", Types.PICKLED_BYTE_ARRAY())

        def process_element1(self, order, context, out):
            order_data = json.loads(order)
            order_id = order_data['id']

            # Store the order in state
            order_state = context.get_state(self.orders_state)
            order_state.update(order_data)

            # Check for a matching shipment
            shipment_state = context.get_state(self.shipments_state)
            if shipment_state.value is not None:
                out.collect(f"Joined: {order_data} with {shipment_state.value}")

        def process_element2(self, shipment, context, out):
            shipment_data = json.loads(shipment)
            order_id = shipment_data['order_id']

            # Store the shipment in state
            shipment_state = context.get_state(self.shipments_state)
            shipment_state.update(shipment_data)

            # Check for a matching order
            order_state = context.get_state(self.orders_state)
            if order_state.value is not None:
                out.collect(f"Joined: {order_state.value} with {shipment_data}")

    joined_stream = orders_stream.connect(shipments_stream) \
        .process(JoinStreams())

    # Print the result of the join
    joined_stream.print()

    # def extract_after_field(kafka_message):
    #     try:
    #         message_json = json.loads(kafka_message)
    #
    #         after_payload = message_json.get('payload', {}).get('after', None)
    #
    #         if after_payload:
    #             return json.dumps(after_payload)  # Return the 'after' field as a string
    #         else:
    #             return None  # No 'after' payload found
    #     except Exception as e:
    #         print(f"Failed to parse message: {kafka_message}, error: {str(e)}")
    #
    #         return None   
    #
    # def extract_after_field_shipment(kafka_message):
    #     try:
    #         message_json = json.loads(kafka_message)
    #
    #         after_payload = message_json.get('payload', {}).get('after', None)
    #
    #         if after_payload:
    #             return json.dumps(after_payload)  # Return the 'after' field as a string
    #         else:
    #             return None  # No 'after' payload found
    #     except Exception as e:
    #         print(f"Failed to parse message: {kafka_message}, error: {str(e)}")
    #
    #         return None   
    #
    # extracted_orders_stream = orders_stream.map(extract_after_field)
    # extracted_shipments_stream = shipments_stream.map(extract_after_field_shipment)
    #
    # class OrdersKeySelector(KeySelector):
    #     def get_key(self, value):
    #         order_data = json.loads(value) 
    #         return order_data.get('id')  # Using 'id' as the key in orders
    #
    # # KeySelector for extracting the 'order_id' from shipments stream
    # class ShipmentsKeySelector(KeySelector):
    #     def get_key(self, value):
    #         shipment_data = json.loads(value)
    #         return shipment_data.get('order_id')  # Using 'order_id' as the key in shipments
    #
    # keyed_orders_stream = extracted_orders_stream.key_by(OrdersKeySelector())
    # keyed_shipments_stream = extracted_shipments_stream.key_by(ShipmentsKeySelector())
    #
    # joined_stream = keyed_orders_stream.join(keyed_shipments_stream) \
    #     .where(OrdersKeySelector()) \
    #     .equal_to(ShipmentsKeySelector()) \
    #     .window(TumblingEventTimeWindows.of(Time.minutes(10))) \
    #     .apply(lambda order, shipment: f"Joined: {order} with {shipment}")
    #
    # # Print the joined result
    # joined_stream.print()
    #
    # # class MyWindowJoinFunction(WindowJoinFunction):
    # #     def join(self, order, shipment,context,collector):
    # #         print(context)
    # #         collector.collect(f"Joined: {order} with {shipment}")
    # #
    # # joined_stream = keyed_orders_stream.connect(keyed_shipments_stream) \
    # #     .where(OrdersKeySelector()) \
    # #     .equalTo(ShipmentsKeySelector()) \
    # #     .window(TumblingEventTimeWindows.of(Time.minutes(10))) \
    # #     .apply(MyWindowJoinFunction())
    # #
    #
    env.execute("Orders and shipment processing jobs")

if __name__ == '__main__':
    main()

