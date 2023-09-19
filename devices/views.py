from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DeviceSerializer
from .models import devices


class DeviceCreateView(APIView):
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
