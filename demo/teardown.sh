kubectl delete -f platform.yaml
helm uninstall my-strimzi-operator -n kafka
kubectl delete namespace kafka