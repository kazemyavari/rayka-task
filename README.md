# Django Restful API Challenge

Implement a simple Restful API on Django using the following tech stack: Python, Django Rest Framework, AWS DynamoDB For Rayka company.

# Getting Started
-   [Installation](#installation)
-   [Usage](#usage)
-   [Test](#test)
-   [Deploy on AWS](#deploy-on-aws-lambda)

## Installation
1. Clone repository:
	```bash
	git clone git@github.com:kazemyavari/rayka-task.git
	cd rayka-task
	```
2. Create a copy of this `env.example` file and name it `.env`. This file will store your actual environment variables. Open the `.env` file in a text editor of your choice and set the values for each variable as required by the project.
	```bash
	cp env.example .env
	```
	
	##### Environment Variables

	Here is a list of environment variables that you need to configure in your `.env` file:

	-   `SECRET_KEY`: Django secret key for security. You should generate a unique secret key and set it here.
    
	- `DEBUG`: Set this to `True` during development to enable debugging features. Set to `False` in production for security reasons.
    
	-   `ALLOWED_HOSTS`: Comma-separated list of allowed hostnames or IP addresses that can access the application. For development, you can use '127.0.0.1,localhost'.

	-   `AWS_ACCESS_KEY`: Your AWS access key for programmatic access to AWS services.
    
	-   `AWS_SECRET_ACCESS`: Your AWS secret access key corresponding to the access key.
    
	-   `AWS_DYNAMODB_REGION_NAME`: The AWS region name where your DynamoDB resources are located.
	-   `AWS_ENDPOINT_LOCAL_URL`: (Optional) If you're using a local version of AWS services (e.g., local DynamoDB), set the endpoint URL here.

> Remember to keep your `.env` file secure and never commit it to
> version control. You should include it in your project's `.gitignore`
> file to prevent accidental exposure of sensitive information.



## Usage
**Method 1: Running the Project with Docker** (Recommended)
- Prerequisites:
	 1. [Docker](https://www.docker.com/get-started)
	 2. [Docker Compose](https://docs.docker.com/compose/install/)
 - Run the Docker Container:
	```bash
	 docker compose up -d
	```
**Method 2: Running the Project with `Django`**
 
1. **Set Up Virtual Environment**:
	 ```bash
	  python -m venv venv
	  source venv/bin/activate # On Windows, use: venv\Scripts\activate
	 ```
2. **Install Dependencies**:
	 ```bash
	  pip install -r requirements.txt
	 ```
3. **Run the Django Server**:
	 ```bash
	  python manage.py runserver
	 ```
##
Your project should now be running, and you can access it at [http://localhost:8000](http://localhost:8000/) in your web browser.

##### API Documentation
Swagger/OpenAPI documentation is available for your APIs. You can access it at:

http://localhost:8000/api/docs/

Use the API documentation to explore and test your APIs interactively.

## Test
To run tests for this project, follow these steps:

**Method 1: Running the Test with Docker**  (Recommended) 	
```bash
 # On Windows:
 docker compose -f docker-compose-test.yml up -d
 python manage.py test
 docker compose -f docker-compose-test.yml down
 # On Linux & Mac:
 ./run_test.sh
```
**Method 2: Running the Test with `Django`**
1. Activate your virtual environment (if not already activated):
	 ```bash
      source venv/bin/activate # On Windows, use: venv\Scripts\activate
	 ```
2. Install test dependencies (if not already installed):
	 ```bash
      pip install -r requirements.txt
	 ```
3. Set up AWS for testing (if applicable):
	 - Option 1: Configure [Local DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html): (Recommended)
	 -  Option 2: AWS Account Configuration
4. Run the tests:
	 ```bash
      python manage.py test
	 ```
## Deploy on AWS lambda

### Zappa - Serverless Python

Zappa makes it super easy to build and deploy server-less, event-driven Python applications (Django or Flask) on AWS Lambda + API Gateway + S3.

-   [https://github.com/zappa/Zappa](https://github.com/zappa/Zappa)

We can deploy our python project on lambda and S3 buckets using zappa in the following three steps :)

    pip install zappa
    zappa init
    zappa deploy