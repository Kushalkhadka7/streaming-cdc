-- Create the database
CREATE DATABASE streaming_analytics;

-- Use the new database
USE streaming_analytics;

CREATE TABLE products (
    id INT PRIMARY KEY,
    name NVARCHAR(100),
    price FLOAT,
    description NVARCHAR(255),
    quantity INT,
    WARRANTY NVARCHAR(255),
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);



USE [streaming_analytics];
GO
EXEC sys.sp_cdc_enable_db;

USE [streaming_analytics];
EXEC sys.sp_cdc_enable_table
    @source_schema = N'dbo',
    @source_name = N'products',
    @role_name = NULL,
    @supports_net_changes = 1;

USE [streaming_analytics];
EXEC sp_configure 'remote access', 1;
RECONFIGURE;
