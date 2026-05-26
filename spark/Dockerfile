FROM apache/spark:3.5.0

USER root

WORKDIR /opt/spark/work-dir

COPY spark-streaming-job.py .

CMD ["/opt/spark/bin/spark-submit", \
     "--master", "spark://spark-master:7077", \
     "--deploy-mode", "client", \
     "/opt/spark/work-dir/spark-streaming-job.py"]
