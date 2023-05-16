### How to to build, run, and test code this application?
 Execute run.sh which will build, run and test all endpoints of the application then remove and clean all of the tested resources. 
###  An example curl request we can use to test against $NAMESPACE.mids255.com/predict that meets your request model in your API.
curl -X 'POST' 'https://giomola.mids255.com/predict' -L -H 'Content-Type: application/json' -d '{"houses":[{"income": 1, "age": 20, "rooms": 3, "beds": 2,"pop":20,"occupants":4,"lat":32.11,"long":11.1},{"income": 1, "age": 30, "rooms": 2, "beds": 1,"pop":10,"occupants":2,"lat":1.1,"long":2.1}]}'
###  What are the downsides of using latest as your docker image tag?
Using latest as the docker image tag removes the granularity and awareness of which version of a docker image is deployed leading to potential bugs or breaking changes not seen in previous versions. It also makes it difficult to roll back to a previous version. 
###  What does kustomize do for us?
Kustomize handles resource management for our app which helps to manage multiple variations of K8 resources across a templated set of yaml files. It also allows us to apply configuration overlays to more simply modify any specific modifications to the base resources. 