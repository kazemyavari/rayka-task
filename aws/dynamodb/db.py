import boto3
import logging
from typing import Dict, List
from django.conf import settings
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)


class DynamoDB:
    def __init__(self, table_name: str, schema: Dict = None):
        self.__table = None
        self.schema = self._set_default_schema() if schema is None else schema
        self.schema["TableName"] = table_name
        self.table_name = table_name

    def _set_default_schema(self) -> dict:
        return {
            "KeySchema": [{"AttributeName": "id", "KeyType": "HASH"}],
            "AttributeDefinitions": [{"AttributeName": "id", "AttributeType": "S"}],
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 10,
                "WriteCapacityUnits": 10,
            },
        }

    @property
    def dynamodb_config(self) -> Dict:
        dynamodb_config = {
            "region_name": settings.AWS_DYNAMODB_REGION_NAME,
            "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
        }

        if settings.AWS_DYNAMODB_REGION_NAME == "local":
            dynamodb_config[
                "endpoint_url"
            ] = f"http://{settings.AWS_LOCAL_DYNAMODB_HOST}:{settings.AWS_LOCAL_DYNAMODB_PORT}"

        return dynamodb_config

    @property
    def dyn_resource(self):
        return boto3.resource("dynamodb", **self.dynamodb_config)

    def exists(self) -> bool:
        try:
            table = self.dyn_resource.Table(self.table_name)
            table.load()
            exists = True
            self.__table = table
        except ClientError as err:
            if err.response["Error"]["Code"] == "ResourceNotFoundException":
                exists = False
            else:
                logger.error(
                    "Couldn't check for existence of %s. Here's why: %s: %s",
                    self.table_name,
                    err.response["Error"]["Code"],
                    err.response["Error"]["Message"],
                )
                raise
        return exists

    def create_table(self):
        if self.exists():
            return None

        try:
            self.__table = self.dyn_resource.create_table(**self.schema)
            self.__table.wait_until_exists()
            return self.__table
        except ClientError as err:
            logger.error(
                "Couldn't create table %s. Here's why: %s: %s",
                self.table_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    @property
    def table(self):
        if self.__table is None:
            self.create_table()

        return self.__table
