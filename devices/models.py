from aws.dynamodb.model import DynamoModel


class Devices(DynamoModel):

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
