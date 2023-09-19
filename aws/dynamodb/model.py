import boto3
import logging
from typing import Dict, List
from django.conf import settings
from botocore.exceptions import ClientError
from boto3.resources.base import ServiceResource

logger = logging.getLogger(__name__)


class DynamoModel:
    """A class for interacting with DynamoDB tables."""

    def __init__(self):
        self._schema_defined()  
        self.table_name = self.schema["TableName"]
        self.table = self.get_table()

    def _schema_defined(self):
        """Ensure that the 'schema' attribute is defined in the child class."""
        if not hasattr(self, "schema"):
            raise AttributeError(
                f"The 'schema' attribute must be defined in the {str(self.table_name).capitalize()} class."
            )
        
        if "TableName" not in self.schema:
            self.schema["TableName"] = self.__class__.__name__

    def _get_config(self) -> Dict:
        """Get the DynamoDB configuration.

        Returns:
            Dict: The DynamoDB configuration.
        """
        dynamodb_config = {
            "region_name": settings.AWS_DYNAMODB_REGION_NAME,
            "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
        }

        if settings.AWS_ENDPOINT_LOCAL_URL:
            dynamodb_config["endpoint_url"] = settings.AWS_ENDPOINT_LOCAL_URL

        return dynamodb_config

    def get_resource(self) -> ServiceResource:
        """Get the DynamoDB resource.

        Returns:
            boto3.resources.base.ServiceResource: The DynamoDB resource.
        """
        return boto3.resource("dynamodb", **self._get_config())

    def get_table(self):
        """Get the DynamoDB table resource, creating it if necessary."""

        try:
            table = self.get_resource().Table(self.table_name)
            table.load()
            return table
        except ClientError as err:
            if err.response["Error"]["Code"] == "ResourceNotFoundException":
                return self.create_table()

            logger.error(
                "Couldn't check for existence of %s. Here's why: %s: %s",
                self.table_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    def create_table(self):
        """Create the DynamoDB table if it doesn't exist."""
        try:
            table = self.get_resource().create_table(**self.schema)
            table.wait_until_exists()
            return table
        except ClientError as err:
            logger.error(
                "Couldn't create table %s. Here's why: %s: %s",
                self.table_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
