-- Create the database
DROP DATABASE streaming_analytics
CREATE DATABASE streaming_analytics
go

-- Use the new database
USE streaming_analytics
go


CREATE TABLE products (
    id INT PRIMARY KEY,
    name NVARCHAR(100),
    price FLOAT,
    description NVARCHAR(255),
    quantity INT,
    WARRANTY NVARCHAR(255),
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
)
go

USE [streaming_analytics]
go

EXEC sys.sp_cdc_enable_db
go

EXEC sys.sp_cdc_enable_table
    @source_schema = N'dbo',
    @source_name = N'products',
    @role_name = NULL,
    @supports_net_changes = 1

EXEC sp_configure 'remote access', 1
RECONFIGURE
go
