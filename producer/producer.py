from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("Producer iniciado...")

while True:
    mensagem = {
        "parque": random.choice(["A", "B", "C"]),
        "ocupacao": random.randint(0, 100),
        "timestamp": time.time()
    }
    producer.send("ocupacao-parques", mensagem)
    producer.flush()
    print("Enviado:", mensagem)
    time.sleep(2)
