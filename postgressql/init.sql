-- Create order table if not exist.
CREATE TABLE IF NOT EXISTS orders (
    id Integer PRIMARY KEY,
    product_id text,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    order_status text,
    order_total text,
    order_quantity text,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- This is needed for debezium to capture the changes.
ALTER TABLE orders REPLICA IDENTITY full;

-- Create shipment table if not exist.
CREATE TABLE IF NOT EXISTS shipments (
    id Integer PRIMARY KEY,
    order_id text,
    tracking_number text,
    shipment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivery_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    shipment_status text,
    shipping_mechanism text,
    shipping_address text,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- This is needed for debezium to capture the changes.
ALTER TABLE shipments REPLICA IDENTITY full;