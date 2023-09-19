import boto3
import logging
from typing import Dict
from django.conf import settings
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)


class DynamoDBMixin:
    def __init__(self):
        self.table_name: str = self.__class__.__name__
        self.table = None
        self._meta_class()
        self.create_table()

    def _meta_class(self):
        if not hasattr(self.__class__, "Meta"):

            class Meta:
                key_schema = [{"AttributeName": "id", "KeyType": "HASH"}]
                attribute_definitions = [{"AttributeName": "id", "AttributeType": "S"}]
                provisioned_throughput = {
                    "ReadCapacityUnits": 10,
                    "WriteCapacityUnits": 10,
                }

            self.__class__.Meta = Meta

        self._meta = self.__class__.Meta

        if not hasattr(self._meta, "key_schema"):
            self._meta.key_schema = [{"AttributeName": "id", "KeyType": "HASH"}]

        if not hasattr(self._meta, "attribute_definitions"):
            self._meta.attribute_definitions = [
                {"AttributeName": "id", "AttributeType": "S"}
            ]

        if not hasattr(self._meta, "provisioned_throughput"):
            self._meta.provisioned_throughput = {
                "ReadCapacityUnits": 10,
                "WriteCapacityUnits": 10,
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
            self.table = table
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
            self.table = self.dyn_resource.create_table(
                TableName=self.table_name,
                KeySchema=self._meta.key_schema,
                AttributeDefinitions=self._meta.attribute_definitions,
                ProvisionedThroughput=self._meta.provisioned_throughput,
            )
            self.table.wait_until_exists()
            return self.table
        except ClientError as err:
            logger.error(
                "Couldn't create table %s. Here's why: %s: %s",
                self.table_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
