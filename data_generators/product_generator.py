from faker import Faker
import pprint
import random
# import pyodbc

# # Database connection details
# server = 'localhost'  # or the server IP/hostname
# database = 'streaming_analytics'
# username = 'sa'
# password = 'admin@123'
# driver = '{ODBC Driver 17 for SQL Server}'  # Change driver if needed

# # Establish the database connection
# connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
# conn = pyodbc.connect(connection_string)
# cursor = conn.cursor()

# # Define the SQL INSERT statement
# sql = """
# INSERT INTO orders (id, name, price, description, quantity, WARRANTY, created_at, updated_at)
# VALUES (?, ?, ?, ?, ?, ?, ?, ?)
# """


import pymssql

# Initialize Faker
fake = Faker()

class Product:
    def generate_products(self, n):
        shipping_types = ['FULL',"HALF","3 MONTHS","6 MONTHS","1 YEAR","2 YEARS","3 YEARS","5 YEARS","10 YEARS"]

        products = []
        for i in range(n):
            product = {
                'id': i,
                'name': fake.word(),
                'price': round(fake.random_number(digits=3), 2),
                'description': fake.paragraph(),
                'quantity': fake.random_number(digits=2),
                'WARRANTY': random.choice(shipping_types),
                'created_at': fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
            }

            products.append(product)
        return products

    def insert_mssql_products(self, products):
        # Establish the connection
        conn = pymssql.connect(server='mssql', user='sa', password='admin@123', database='streaming_analytics')
        cursor = conn.cursor()

        pprint.pprint(products,indent=4)
        # Insert data into a table
        sql = "INSERT INTO dbo.products (id, name, price, description, quantity, WARRANTY, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
       
        values = [
            (
                item['id'],
                item['name'],
                item['price'],
                item['description'],
                item['quantity'],
                item['WARRANTY'],
                item['created_at'],
                item['updated_at']
            )
            for item in products
        ]
        cursor.executemany(sql, values)

        # Commit the transaction
        conn.commit()

        # Close the connection
        cursor.close()

    def insert_products(self, products):
        # Batch size
        batch_size = 10  # Adjust batch size based on your needs

        # Execute batch insert
        try:
            for i in range(0, len(product_data), batch_size):
                batch = product_data[i:i+batch_size]

                cursor.executemany(sql, batch)
            
            # Commit the transaction
            conn.commit()
            print('Batch insert completed successfully.')

        except Exception as e:
            print(f'Error occurred: {e}')

            conn.rollback()

        finally:
            # Close the connection
            cursor.close()
            conn.close()


if __name__ == "__main__":
    pprint.pprint('Product Generator------->')
    # Generate products
    product = Product()
    generated_products = product.generate_products(100)
    product.insert_mssql_products(generated_products)

    
    