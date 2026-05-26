FROM python:3.10-slim

WORKDIR /app

COPY consumer.py .

RUN pip install kafka-python boto3

CMD ["python", "-u", "consumer.py"]
