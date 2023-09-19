from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView, exception_handler
from .serializers import DeviceSerializer
from .models import devices


class DeviceCreateView(APIView):
    """Create a new device.

    This view allows the creation of a new device by sending a POST request
    with the required data in the request body.

    Parameters:
    - serializer_class: The serializer class to use for validation and serialization.

    Returns:
    - Response: An HTTP response indicating the result of the operation.
    """

    serializer_class = DeviceSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "message": "Item created successfully.",
                "data": serializer.validated_data,
            },
        )


class DeviceRetrieveView(APIView):
    """Retrieve a device by its ID.

    This view allows the retrieval of a device by sending a GET request
    with the device's ID as part of the URL.

    Parameters:
    - serializer_class: The serializer class to use for validation and serialization.

    Returns:
    - Response: An HTTP response containing the device data or an error message.
    """

    serializer_class = DeviceSerializer

    def get(self, request, pk):
        device = devices.table.get_item(Key={"id": f"/devices/id{pk}"})

        if not "Item" in device:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": "This item does not exist."},
            )

        serializer = self.serializer_class(device["Item"])
        return Response(status=status.HTTP_200_OK, data={"data": serializer.data})


def custom_exception_handler(exc, context):
    """
    Custom exception handler for handling uncaught exceptions.

    This function handles uncaught exceptions and returns a custom
    HTTP 500 Internal Server Error response with an error message.

    Args:
    - exc: The exception that occurred.
    - context: The context of the exception.

    Returns:
    - Response: An HTTP response indicating the error with status 500.
    """
    response = exception_handler(exc, context)
    if response is None:
        response = Response(
            {"message": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return response
