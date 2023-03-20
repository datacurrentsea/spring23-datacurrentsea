### How to to build, run, and test code this application?
 Execute run.sh which will build, run and test all endpoints of the application then remove and clean all of the tested resources. 
 ### Questions:
 #### What are the benefits of caching?
The benefits of caching allow users to receive faster respones from an api endpoint call given someone else has previously requested the same call. This is also helpful for the api server in regards to putting less api resources to work given the same processing was done in a prior call. In short this helps performance, server load and user experience. 
 #### What is the difference between Docker and Kubernetes?
Docker is a containerization application that helps package applications in reproduceable manner such that the application can run anwhere regardless of the infrastructure its sitting on. Kubernetes is an orchestration platform that helps deploy and manage containerized applications. Kubernetes helps developers scale, update and load balance an application which helps with the management overhead of deploying applications. 
 #### What does a kubernetes deployment do?
 A kubernetes deployment manages the deployment of identical pods in and ensures they are up and running. The deployment allows you to define the number of replicas, which container image to run and assists in updating pods within a deployment. 
 #### What does a kubernetes service do?
 A kubernetes service defines the service that exposes pods to the network. A service can be defined as a cluster ip, node port or load balancer and determines which port can be used to interface with the pods within that service.