import boto3
import logging
from typing import Dict, List
from django.conf import settings
from botocore.exceptions import ClientError
from boto3.resources.base import ServiceResource

logger = logging.getLogger(__name__)


class DynamoDB:
    """A class for interacting with DynamoDB tables."""

    def __init__(self, table_name: str, schema: Dict = None):
        """Initialize a DynamoDB instance.

        Args:
            table_name (str): The name of the DynamoDB table.
            schema (Dict, optional): The schema definition for the table. Defaults to None.
        """
        self.__table = None
        self.schema = self._set_default_schema() if schema is None else schema
        self.schema["TableName"] = table_name
        self.table_name = table_name

    def _set_default_schema(self) -> dict:
        """
        Set default schema for a DynamoDB table.

        Returns:
            dict: The default schema.
        """
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
        """Get the DynamoDB configuration.

        Returns:
            Dict: The DynamoDB configuration.
        """
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
    def dyn_resource(self) -> ServiceResource:
        """
        Get the DynamoDB resource.

        Returns:
            boto3.resources.base.ServiceResource: The DynamoDB resource.
        """
        return boto3.resource("dynamodb", **self.dynamodb_config)

    def exists(self) -> bool:
        """Check if the DynamoDB table exists.

        Returns:
            bool: True if the table exists, False otherwise.
        """
        try:
            table = self.dyn_resource.Table(self.table_name)
            table.load()
            self._table = table
            return True
        except ClientError as err:
            if err.response["Error"]["Code"] == "ResourceNotFoundException":
                return False

            logger.error(
                "Couldn't check for existence of %s. Here's why: %s: %s",
                self.table_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    def create_table(self):
        """Create the DynamoDB table if it doesn't exist."""
        if self.exists():
            return None

        try:
            self._table = self.dyn_resource.create_table(**self.schema)
            self._table.wait_until_exists()
            return self._table
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
        """Get the DynamoDB table resource, creating it if necessary."""

        if self._table is None:
            self.create_table()

        return self._table
