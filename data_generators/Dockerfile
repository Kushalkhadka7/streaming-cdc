FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libsqlite3-dev \
    libssl-dev \
    libffi-dev \
    unixodbc \
    python3-dev

RUN pip install faker
RUN pip install sqlalchemy pymssql 
RUN pip install psycopg2-binary

RUN export LD_LIBRARY_PATH=/opt/microsoft/msodbcsql17/lib64/:$LD_LIBRARY_PATH

CMD ["python"]