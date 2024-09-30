FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libsqlite3-dev \
    libssl-dev \
    libffi-dev \
    unixodbc \
    python3-dev

COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN export LD_LIBRARY_PATH=/opt/microsoft/msodbcsql17/lib64/:$LD_LIBRARY_PATH

CMD ["python"]
