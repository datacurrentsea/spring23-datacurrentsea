# Build Docker image for 255_lab1
docker build -t 255_lab1 .
# Run Docker container for 255_lab1 image
docker run -d --name 255_lab1_container --rm -d -p 8000:8000 255_lab1

#container_name="255_lab1_container"
#container_status = $(docker inspect --format='{{json .State.Health.Status}}' 255_lab1_container)
#while [$container_status != "\"healthy\""]; do
#    echo "Container is starting"
#    container_status=$(docker inspect --format='{{json .State.Health.Status}}' 255_lab1_container)
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

echo "Tests are complete!"

echo "Stopping and removing Container"
docker stop 255_lab1_container
docker image rm $(docker images -f "dangling=true" -q)