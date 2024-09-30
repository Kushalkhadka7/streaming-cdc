import os
import time
import pprint
import random
import psycopg2

from faker import Faker
from pathlib import Path
from psycopg2 import sql
from dotenv import load_dotenv


class Order:
    def __init__(self) -> None:
        self.fake = Faker()

    def generate_fake_orders_shipments(self):

        order_status = ["PENDING", "SHIPPED", "DELIVERED", "RETURNED"]
        shipping_mechanism = ["UPS", "FedEx", "DHL", "USPS", "Amazon"]
        shipment_status = ["PENDING", "SHIPPED", "DELIVERED", "RETURNED"]

        order = {
            "id": self.fake.random_number(digits=5),
            "product_id": random.randint(1, 10),
            "order_date": self.fake.date_time_this_year().strftime("%Y-%m-%d %H:%M:%S"),
            "order_status": random.choice(order_status),
            "order_total": random.randint(100, 1000),
            "order_quantity": random.randint(1, 10),
            "created_at": self.fake.date_time_this_year().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.fake.date_time_this_year().strftime("%Y-%m-%d %H:%M:%S"),
        }

        shipment = {
            "id": self.fake.random_number(digits=5),
            "order_id": order["id"],
            "tracking_number": self.fake.random_number(digits=10),
            "shipment_date": self.fake.date_time_this_year().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "delivery_date": self.fake.date_time_this_year().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "shipment_status": random.choice(shipment_status),
            "shipping_mechanism": random.choice(shipping_mechanism),
            "shipping_address": self.fake.address(),
            "created_at": self.fake.date_time_this_year().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.fake.date_time_this_year().strftime("%Y-%m-%d %H:%M:%S"),
        }

        return {"order": order, "shipment": shipment}


def get_config():
    PSQL_USER = os.getenv("PSQL_USER")
    PSQL_PASSWORD = os.getenv("PSQL_PASSWORD")
    PSQL_DATABASE = os.getenv("PSQL_DATABASE")
    PSQL_HOST = os.getenv("PSQL_HOST")

    return {
        "PSQL_PASSWORD": PSQL_PASSWORD,
        "PSQL_USER": PSQL_USER,
        "PSQL_DATABASE": PSQL_DATABASE,
        "PSQL_HOST": PSQL_HOST,
    }


def get_credentials():
    config = get_config()

    return {
        "dbname": config.get("PSQL_DATABASE"),
        "user": config.get("PSQL_USER"),
        "password": config.get("PSQL_PASSWORD"),
        "host": config.get("PSQL_HOST"),
        "port": 5432,
    }


if __name__ == "__main__":
    db_credentials = get_credentials()
    conn = psycopg2.connect(**db_credentials)
    cursor = conn.cursor()

    orderInstance = Order()

    insert_order_query = """
        INSERT INTO public.orders
            (id, product_id, order_date, order_status, order_total, order_quantity, created_at, updated_at)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    insert_shipment_query = """
        INSERT INTO public.shipments
            (id, order_id, tracking_number, shipment_date, delivery_date, shipment_status, shipping_mechanism,shipping_address, created_at, updated_at)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    while True:
        try:
            generated_orders = orderInstance.generate_fake_orders_shipments()

            processed_order = (
                generated_orders["order"]["id"],
                generated_orders["order"]["product_id"],
                generated_orders["order"]["order_date"],
                generated_orders["order"]["order_status"],
                generated_orders["order"]["order_total"],
                generated_orders["order"]["order_quantity"],
                generated_orders["order"]["created_at"],
                generated_orders["order"]["updated_at"],
            )

            processed_shipment = (
                generated_orders["shipment"]["id"],
                generated_orders["shipment"]["order_id"],
                generated_orders["shipment"]["tracking_number"],
                generated_orders["shipment"]["shipment_date"],
                generated_orders["shipment"]["delivery_date"],
                generated_orders["shipment"]["shipment_status"],
                generated_orders["shipment"]["shipping_mechanism"],
                generated_orders["shipment"]["shipping_address"],
                generated_orders["shipment"]["created_at"],
                generated_orders["shipment"]["updated_at"],
            )

            pprint.pprint(f"order_id: {generated_orders['order']}")
            pprint.pprint(f"shipment_id: {generated_orders['shipment']}")

            cursor.execute(insert_order_query, processed_order)
            cursor.execute(insert_shipment_query, processed_shipment)

            # Commit the transaction
            conn.commit()

            time.sleep(10)
        except Exception as e:
            pprint.pprint(e)

            conn.rollback()

            time.sleep(10)
