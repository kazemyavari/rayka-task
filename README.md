# Django Restful API Challenge

Implement a simple Restful API on Django using the following tech stack: Python, Django Rest Framework, AWS DynamoDB For Rayka company

## Getting Started
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Test](#test)
 
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

# Uncomment the following line if running locally with DynamoDB Local
# AWS_ENDPOINT_LOCAL_URL=http://localhost:8000
```

### 3. Start the Docker containers:
```bash
>>> docker compose up -d
```

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