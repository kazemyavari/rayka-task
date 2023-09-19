from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DeviceSerializer
from .models import devices


class DeviceCreateView(APIView):
    serializer_class = DeviceSerializer

    def post(self, request):
        try:
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
        except Exception as e:
            return Response(
                {"error": "Internal Server Error", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DeviceRetrieveView(APIView):
    serializer_class = DeviceSerializer

    def get(self, request, pk):
        try:
            device = devices.table.get_item(Key={"id": f"/devices/id{pk}"})

            if not "Item" in device:
                return Response(
                    status=status.HTTP_404_NOT_FOUND,
                    data={"message": "This item does not exist."},
                )

            serializer = self.serializer_class(device["Item"])
            return Response(status=status.HTTP_200_OK, data={"data": serializer.data})
        except Exception as e:
            return Response(
                {"error": "Internal Server Error", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
