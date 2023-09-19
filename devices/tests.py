from rest_framework import status
from rest_framework.test import APIClient, APISimpleTestCase
from parameterized import parameterized
from django.test import override_settings


class DeviceCreateRetrieveTest(APISimpleTestCase):
    def setUp(self):
        self.client = APIClient()

    @parameterized.expand(
        [
            (
                "valid_device",
                {
                    "id": "/devices/id1",
                    "deviceModel": "/devicemodels/id1",
                    "name": "Sensor",
                    "note": "Testing a sensor.",
                    "serial": "A020000102",
                },
                status.HTTP_201_CREATED,
            ),
            (
                "duplicate_device",
                {
                    "id": "/devices/id1",  # ID must be unique and non-repeating.
                    "deviceModel": "/devicemodels/id1",
                    "name": "Sensor",
                    "note": "Testing a sensor.",
                    "serial": "A020000102",
                },
                status.HTTP_400_BAD_REQUEST,
            ),
            (
                "invalid_device_id",
                {
                    "id": "id50",  # id format is invalid : must be in this format => /devices/id<pk>
                    "deviceModel": "/devicemodels/id1",
                    "name": "Sensor",
                    "note": "Testing a sensor.",
                    "serial": "A020000102",
                },
                status.HTTP_400_BAD_REQUEST,
            ),
            (
                "invalid_device_id",
                {
                    "id": "/devices/id10",
                    "deviceModel": "id1",  # deviceModel format is invalid : must be in this format => /devicemodels/id<int>
                    "name": "Sensor",
                    "note": "Testing a sensor.",
                    "serial": "A020000102",
                },
                status.HTTP_400_BAD_REQUEST,
            ),
            (
                "missing_data",
                {
                    "id": "/devices/id2",
                    "deviceModel": "/devicemodels/id2",
                    "name": "Sensor",
                    "note": "Testing a sensor without serial.",
                    # serial required field
                },
                status.HTTP_400_BAD_REQUEST,
            ),
        ]
    )
    @override_settings(AWS_LOCAL_DYNAMODB_PORT=4000)
    def test_create_device(self, name, device_data, expected_status):
        response = self.client.post("/api/devices/", device_data, format="json")
        self.assertEqual(response.status_code, expected_status)

    @parameterized.expand(
        [
            ("existing_device", 1, status.HTTP_200_OK),
            ("nonexistent_device", 1000, status.HTTP_404_NOT_FOUND),
        ]
    )
    @override_settings(AWS_LOCAL_DYNAMODB_PORT=4000)
    def test_retrieve_device(self, name, device_id, expected_status):
        response = self.client.get(f"/api/devices/{device_id}/")
        self.assertEqual(response.status_code, expected_status)
