# Move directory to lab2
cd lab2
# Train model 
poetry run python trainer/train.py 

mv model_pipeline.pkl model_pipeline.pkl

# Build Docker image for 255_lab2
docker build -t 255_lab2 .
# Run Docker container for 255_lab2 image
docker run -d --name 255_lab2_container --rm -d -p 8000:8000 255_lab2

#container_name="255_lab2_container"
#container_status = $(docker inspect --format='{{json .State.Health.Status}}' 255_lab2_container)
#while [$container_status != "\"healthy\""]; do
#    echo "Container is starting"
#    container_status=$(docker inspect --format='{{json .State.Health.Status}}' 255_lab2_container)
#done
#echo "Container status is healthy"
sleep 10
# Test endpoints with curl
echo "testing '/hello' endpoint with ?name=Winegar"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?name=Winegar"

echo "testing '/' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/"

echo "testing '/docs' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/docs"

echo "testing '/health' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/health"

echo "testing '/predict' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X POST "http://localhost:8000/predict" -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"income":10,"age":20,"rooms":4,"beds":3,"pop":10,"occupants":2,"lat":37.88,"long":-122.23}'
echo "Tests are complete!"

echo "Stopping and removing Container"
docker stop 255_lab2_container
docker image rm $(docker images -f "dangling=true" -q)