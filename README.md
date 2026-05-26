Para ativar o ambiente virtual: 
.\venv\Scripts\activate

Para aceder à consola do minio é necessário criar um túnel, uma vez que estou a correr o minikube dentro do docker/WSL2 no windows, através de:
minikube service minio-service

kubectl port-forward svc/spark-master 8080:8080, para aceder ao spark master
kubectl exec -it spark-master-598dc88755-5hxkc -- /opt/spark/bin/spark-submit `
  --master spark://spark-master:7077 `
  --deploy-mode client `
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262 `
  --conf spark.jars.ivy=/tmp/.ivy2 `
  /opt/spark/work-dir/spark-streaming-job.py

kubectl delete deployment kafka
kubectl delete deployment zookeeper
kubectl delete svc kafka
kubectl delete svc zookeeper

kubectl apply -f kafka/zookeeper-deployment.yaml
kubectl apply -f kafka/zookeeper-service.yaml

kubectl apply -f kafka/kafka-deployment.yaml
kubectl apply -f kafka/kafka-service.yaml

kubectl exec -it spark-master-598dc88755-5hxkc -- ls /opt/spark/work-dir


kubectl exec -it kafka-545776f776-mhwc2 -- /bin/kafka-console-producer --bootstrap-server localhost:9092 --topic parques-vaga
{"id": 10, "nome": "Parque Norte", "vagas": 15}
{"id": 11, "nome": "Parque Oriente", "vagas": 30}
{"id": 12, "nome": "Parque das Nações", "vagas": 100}
{"id": 13, "nome": "Parque Tejo", "vagas": 5}
{"id": 14, "nome": "Parque Expo", "vagas": 20}

kubectl exec -it spark-master-598dc88755-5hxkc -- /opt/spark/bin/spark-submit `
  --master local[1] `
  --conf "spark.jars.ivy=/tmp/.ivy2" `
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262 `
  /opt/spark/work-dir/spark-streaming-job.py