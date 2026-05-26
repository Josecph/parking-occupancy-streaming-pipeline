FROM apache/spark:3.5.0

USER root

WORKDIR /opt/spark-app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY spark-streaming-job.py .

CMD ["/opt/spark/bin/spark-submit", \
     "--master", "spark://spark-master:7077", \
     "--deploy-mode", "client", \
     "/opt/spark-app/spark-streaming-job.py"]
