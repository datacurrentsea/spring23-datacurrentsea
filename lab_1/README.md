 # About this application
 ### What this application does:
 #### This application serves a restful 'hello' endpoint for users to engage with and get their name as response. It also comes with a /docs endpoint for more information about how to make restful requests to this app.
 ### How to build and run this application:
 #### 1. Git clone this repo. 
 git clone https://github.com/datacurrentsea/spring23-datacurrentsea.git
 #### 2. cd into the repo. 
 cd spring23-datacurrentsea/lab_1/lab1
 #### 3. build the image
 docker build -t 255_lab1 .
 #### 4. run the container 
 docker run -d --name 255_lab1_container --rm -d -p 8000:8000 255_lab1
 #### 5. Check for healthy status in the container
 docker ps -a
 #### 6. Navigate to the link below and verify you see {'hello': 'world'}
 http://localhost:8000/hello?name=world 
 ### How to test this application?
 Execute run.sh which will build, run and test 3 endpoints of the application then remove and clean all of the tested resources. 
 ### Questions:
 #### What status code should be raised when a query parameter does not match our expectations?
 A 404 status code should be raised when the requested parameter that was sent in the query parameter does not exist. This indicates that something is wrong with the input that was provided the endpoint and another type of input or formatting is required. Referencing the /docs for the endpoint can provide more clarification on an example of the correct query parameters. 
 #### What does Python Poetry handle for us?
 Poetry handles version dependencies of specific python libraries associated with this application. This ensures no conflicting versions are built when reproducing this application with tools like docker. Poetry is also helpful for compatibility checks between package versions when using the poetry update command which checks all compatibility tables before any package versions are changed. 
 #### What advantages do multi-stage docker builds give us?
 The advantages of multi-stage docker builds provides us with a smaller disk footprint when building images that containers will use when running applications. Multi-stage builds also reduce the number of dependencies and packages needed for the image which limits the attack surface of the application and improves the security posture. This is also helpful when debugging particular stages in the build process. 