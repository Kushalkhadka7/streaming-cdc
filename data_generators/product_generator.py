import os
import pprint
import random
import pymssql

from faker import Faker
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path(".env.products")
load_dotenv(dotenv_path=dotenv_path)


class Product:
    def __init__(self) -> None:
        self.fake = Faker()

    def generate_fake_products(self, n):
        shipping_types = [
            "FULL",
            "HALF",
            "3 MONTHS",
            "6 MONTHS",
            "1 YEAR",
            "2 YEARS",
            "3 YEARS",
            "5 YEARS",
            "10 YEARS",
        ]

        products = []
        for i in range(n):
            product = {
                "id": i,
                "name": self.fake.word(),
                "description": self.fake.paragraph(),
                "WARRANTY": random.choice(shipping_types),
                "quantity": self.fake.random_number(digits=2),
                "price": round(self.fake.random_number(digits=3), 2),
                "created_at": self.fake.date_time_this_year().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "updated_at": self.fake.date_time_this_year().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            }

            products.append(product)
        return products

    def get_credentials(self):
        MSSQL_SERVER = os.getenv("MSSQL_SERVER")
        MSSQL_USER = os.getenv("MSSQL_USER")
        MSSQL_PASSWORD = os.getenv("MSSQL_PASSWORD")
        MSSQL_DATABASE = os.getenv("MSSQL_DATABASE")

        return {
            "MSSQL_SERVER": MSSQL_SERVER,
            "MSSQL_PASSWORD": MSSQL_PASSWORD,
            "MSSQL_USER": MSSQL_USER,
            "MSSQL_DATABASE": MSSQL_DATABASE,
        }

    def get_db_connection(self):
        config = self.get_credentials()

        conn = pymssql.connect(
            server=config.get("MSSQL_SERVER",""),
            user=config.get("MSSQL_USER",""),
            password=config.get('MSSQL_PASSWORD',''),
            database=config.get('MSSQL_DATABASE',''),
        )
        cursor = conn.cursor()

        return {cursor, conn}

    def insert_products(self, products):
        cursor, conn = self.get_db_connection()

        # Insert data into a table
        sql = """
            INSERT INTO dbo.products
                (id, name, price, description, quantity, WARRANTY, created_at, updated_at)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = [
            (
                item["id"],
                item["name"],
                item["price"],
                item["description"],
                item["quantity"],
                item["WARRANTY"],
                item["created_at"],
                item["updated_at"],
            )
            for item in products
        ]

        cursor.executemany(sql, values)

        # Commit the transaction
        conn.commit()

        # Close the connection
        cursor.close()

        exit()


if __name__ == "__main__":
    pprint.pprint("******************* Generating products data *******************")

    product = Product()
    generated_products = product.generate_fake_products(100)
    product.insert_products(generated_products)

    pprint.pprint(
        "******************* Successfully populated products data *******************"
    )
