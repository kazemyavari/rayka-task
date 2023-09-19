import boto3
import logging
from typing import Dict
from django.conf import settings
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)


class DynamoDBMixin:
    def __init__(self):
        self.table_name: str = self.__class__.__name__
        self._meta = self.__class__.Meta
        self.table = None

        self._meta_class_exists()

    def _meta_class_exists():
        if not hasattr(self.__class__, "Meta"):
            raise Exception(f"{self.table_name} Class must have Attribute Meta Class.")

        must_attrs = ["key_schema", "attribute_definitions", "provisioned_throughput"]
        for attr in must_attrs:
            if not hasattr(self.__class__._meta, attr):
                raise Exception(f"Meta Class must have Attribute {attr}.")

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
