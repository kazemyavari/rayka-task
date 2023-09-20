# Django Restful API Challenge

Implement a simple Restful API on Django using the following tech stack: Python, Django Rest Framework, AWS DynamoDB For Rayka company

## Getting Started
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Test](#test)
- [DynamoDB](#dynamodb)
 
## Prerequisites

Before you begin, make sure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Installation

### 1. Clone repository:
```bash
>>> git clone git@github.com:kazemyavari/rayka-task.git
>>> cd rayka-task
```

### 2. Change .env file for environment variables (if needed): 

#### Update the .env file with your configuration, including:

```bash
# AWS credentials (for AWS services)
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key

>>> If you want to switch back to using DynamoDB Local for local development,
you can comment out the AWS credentials and uncomment the AWS_ENDPOINT_LOCAL_URL line in the .env file 
and restart the project as needed.
# Uncomment the following line if running locally with DynamoDB Local
# AWS_ENDPOINT_LOCAL_URL=http://localhost:8000

>>> Of course, it is better not to use Docker and run the project as follows:
>>> python manage.py runserver
```

### 3. Start the Docker containers:
```bash
>>> docker compose up -d
```
## Usage

### API Documentation
Swagger/OpenAPI documentation is available for your APIs. You can access it at:

http://localhost:8000/api/docs/

Use the API documentation to explore and test your APIs interactively.

## Test

### Windows:
```bash
>>> docker compose -f docker-compose-test.yml up -d
>>> python manage.py test
>>> docker compose -f docker-compose-test.yml down
```

### Linux & Mac:
```bash
>>> ./run_test.sh
```

## DynamoDB

### DynamoDB Tables

In this project, DynamoDB tables are automatically created based on the schema definition you provide. You don't need to create the tables manually; the necessary tables are provisioned when you run the project.

### Creating a DynamoDB Model

To define a DynamoDB model for your data, you can use the `DynamoModel` class provided in the `aws.dynamodb.model` module. Here's an example of how to create a model for the `YourModel` table:

```python
from aws.dynamodb.model import DynamoModel

class YourModel(DynamoModel):
    schema = {
        "KeySchema": [
            {"AttributeName": "id", "KeyType": "HASH"},
        ],
        "AttributeDefinitions": [{"AttributeName": "id", "AttributeType": "S"}],
        "ProvisionedThroughput": {
            "ReadCapacityUnits": 10,
            "WriteCapacityUnits": 10,
        },
    }

devices = Devices()
```