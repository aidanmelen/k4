kubectl create namespace kafka
helm repo add strimzi https://strimzi.io/charts/
helm install my-strimzi-operator strimzi/strimzi-kafka-operator -n kafka
kubectl apply -f platform.yaml
kubectl wait --for=condition=Ready kafka/my-cluster --timeout=1m -n kafka
# kubectl port-forward svc/my-cluster-kafka-brokers 9090:9090 -n kafka