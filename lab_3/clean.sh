kubectl delete all --all -n w255
echo "Confirming all resources are removed"
kubectl get all -n w255
echo "Stopping minikube"
minikube stop
minikube delete
minikube cache delete
rm -rf ~/.minikube
