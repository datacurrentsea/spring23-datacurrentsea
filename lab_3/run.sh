# Ensure model is trained
# 1. Move directory to lab3
cd lab3
# 2. Train model 
poetry run python trainer/train.py 
# 3. Move pkl file 
mv model_pipeline.pkl model_pipeline.pkl
# Start minikube 
minikube start --kubernetes-version=v1.25.4
# Setup docker env to build docker daemon with minikube
eval $(minikube docker-env)
# Build Docker image for 255_lab3
docker build . -t 255-lab3-app
# Apply k8 namespace
kubectl apply -f infra/namespace.yaml
# Set context 
kubectl config set-context --current --namespace=w255
# Apply Deployments
kubectl apply -f infra/deployment-redis.yaml
kubectl apply -f infra/deployment-pythonapi.yaml
# Apply Services
kubectl apply -f infra/service-redis.yaml
kubectl apply -f infra/service-prediction.yaml
# Wait for pods to be ready
kubectl wait --for=condition=Ready pod -l app=255-lab3-app -n w255
# Port forward 8000
kubectl port-forward service/prediction-service 8000:8000 &
# LAB2 -Run Docker container for 255_lab3 image
#docker run -d --name 255_lab3_container --rm -d -p 8000:8000 255_lab3
# Wait for api to be accessible
#while ! nc -z localhost 8000; do echo "Service is not yet running on port 8000, waiting...";sleep 5;done
#sleep 30
# Test endpokubints with curl
echo "testing '/hello' endpoint with ?name=Winegar"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?name=Winegar"

echo "testing '/' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/"

echo "testing '/docs' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/docs"

echo "testing '/health' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/health"

echo "testing '/predict' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X POST "http://localhost:8000/predict" -H 'accept: application/json' -H 'Content-Type: application/json' -d '
{"houses":[{"income": 1, "age": 20, "rooms": 3, "beds": 2,"pop":20,"occupants":4,"lat":32.11,"long":11.1},{"income": 1, "age": 30, "rooms": 2, "beds": 1,"pop":10,"occupants":2,"lat":1.1,"long":2.1}]}'
echo "Tests are complete!"

echo "Getting all resources in the 255 name-space"
kubectl get all -n w255
echo "Stopping and removing resources in 255 name-space"
kubectl delete all --all -n w255
echo "Confirming all resources are removed"
kubectl get all -n w255
echo "Stopping minikube"
minikube stop
minikube delete
minikube cache delete
rm -rf ~/.minikube