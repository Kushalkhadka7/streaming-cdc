curl -X POST -H "Content-Type: application/json" --data @register-sql-server.json http://localhost:8094/connectors &&
curl -X POST -H "Content-Type: application/json" --data @register-psql-server.json http://localhost:8094/connectors