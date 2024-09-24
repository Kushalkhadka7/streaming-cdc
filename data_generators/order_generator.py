from faker import Faker
import pprint
import random
import time

import psycopg2
from psycopg2 import sql

# Define connection parameters
conn_params = {
    'dbname': 'streaming-analytics',
    'user': 'admin',
    'password': 'admin',
    'host': 'postgres',
    'port': '5432'
}

fake  = Faker()

class Order:
    def generate_orders(self):

        order_status = ['PENDING', 'SHIPPED', 'DELIVERED', 'RETURNED']
        shipping_mechanism = ['UPS', 'FedEx', 'DHL', 'USPS', 'Amazon']
        shipment_status = ['PENDING', 'SHIPPED', 'DELIVERED', 'RETURNED']

 
        order = {
            'id': fake.random_number(digits=5),
            'product_id': random.randint(1, 10),
            'order_date': fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),
            'order_status': random.choice(order_status),
            'order_total': random.randint(100, 1000),
            'order_quantity':random.randint(1, 10),
            'created_at': fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
        }

        shipment = {
            'id': fake.random_number(digits=5),
            'order_id' : order['id'],   
            "tracking_number" :fake.random_number(digits=10),
            'shipment_date': fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),
            'delivery_date': fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),
            'shipment_status': random.choice(shipment_status),
            'shipping_mechanism': random.choice(shipping_mechanism),
            "shipping_address": fake.address(),   
            'created_at': fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
        }

        return {"order":order,"shipment":shipment}

          

if __name__ == '__main__':
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()

    orderInstance = Order()

    insert_order_query = """
        INSERT INTO public.orders (id, product_id, order_date, order_status, order_total, order_quantity, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    insert_shipment_query = """
        INSERT INTO public.shipments (id, order_id, tracking_number, shipment_date, delivery_date, shipment_status, shipping_mechanism,shipping_address, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    while True:
        try:
            generated_orders = orderInstance.generate_orders()

            order_tuple = (
                generated_orders['order']['id'],
                generated_orders['order']['product_id'],
                generated_orders['order']['order_date'],
                generated_orders['order']['order_status'],
                generated_orders['order']['order_total'],
                generated_orders['order']['order_quantity'],
                generated_orders['order']['created_at'],
                generated_orders['order']['updated_at']
            )

            shipment_tuple =(
                generated_orders['shipment']['id'],
                generated_orders['shipment']['order_id'],
                generated_orders['shipment']['tracking_number'],
                generated_orders['shipment']['shipment_date'],
                generated_orders['shipment']['delivery_date'],
                generated_orders['shipment']['shipment_status'],
                generated_orders['shipment']['shipping_mechanism'],
                generated_orders['shipment']['shipping_address'],
                generated_orders['shipment']['created_at'],
                generated_orders['shipment']['updated_at']
            )

            pprint.pprint(generated_orders, indent=4)
            cursor.execute(insert_order_query,order_tuple)
            cursor.execute(insert_shipment_query, shipment_tuple)

            # Commit the transaction
            conn.commit()

            time.sleep(10)
        except Exception as e:
            print(e)
            conn.rollback()
            time.sleep(10)
   
   
