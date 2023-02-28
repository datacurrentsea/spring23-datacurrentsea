 # About this application
 ### What this application does:
 #### This application serves a restful 'hello' endpoint for users to engage with and get their name as response. It also comes with a /docs endpoint for more information about how to make restful requests to this app. In addition to the above this app provides a '/predict' endpoint that will predict the price of a home based on the housing characteristics passed the model. It also comes with a '/health' endpoint that returns the UTC time that a get request was made. 
 ### How to build and run this application:
 #### 1. Git clone this repo. 
 git clone https://github.com/datacurrentsea/spring23-datacurrentsea.git
 #### 2. cd into the repo. 
 cd spring23-datacurrentsea/lab_2/lab2
 #### 3. build the image
 docker build -t 255_lab2 .
 #### 4. run the container 
 docker run -d --name 255_lab2_container --rm -d -p 8000:8000 255_lab2
 #### 5. Check for healthy status in the container
 docker ps -a
 #### 6. Navigate to the link below and verify you see the time
 http://localhost:8000/health 

 ### How to test this application?
 Execute run.sh which will build, run and test all endpoints of the application then remove and clean all of the tested resources. 
 ### Questions:
 #### What does Pydantic handle for us?
 Pydantic handles the input and output schema and type validation for data that is passed and generated from api requests and responses. Pydantic will deny requests if the validation of the input model is not met and automatically provide detailed error messages as a response to the user so that they know what needs to be fixed or modified. 
 #### What does Github Actions do?
Github actions handle a series of different automated actions that are configurable within the CI/CD pipeline. In our case it provides us with the verification that Pytests successfully run on the latest committed code before code is pulled down which ensure that only code that passes all the necessary tests gets pulled from the origin repo. 
 #### Describe what the Sequence Diagram below shows. 
 The squence diagram depicts a user who sends a post request to the API and if that data is missing any required fields or has incorrect data types it will return an error. If the data is formatted correctly it gets passed to the model and the model returns a prediction to the user. 