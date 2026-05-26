from kafka import KafkaConsumer
import json
import boto3
import time

consumer = KafkaConsumer(
    "ocupacao-parques",
    bootstrap_servers="kafka:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="consumer-parques",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)


s3 = boto3.client(
    "s3",
    endpoint_url="http://minio-service:9000",
    aws_access_key_id="admin",
    aws_secret_access_key="admin123"
)

bucket = "raw-ingest"

print("Consumer iniciado...")

for msg in consumer:
    try:
        dados = msg.value
        print("Recebido:", dados)

        nome_ficheiro = f"registos/{int(time.time())}.json"

        s3.put_object(
            Bucket=bucket,
            Key=nome_ficheiro,
            Body=json.dumps(dados)
        )

    except Exception as e:
        print("Erro no consumer:", e)
        time.sleep(2)

