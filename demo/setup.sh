kubectl create namespace kafka
helm repo add strimzi https://strimzi.io/charts/
helm install my-strimzi-operator strimzi/strimzi-kafka-operator -n kafka
kubectl apply -f platform.yaml