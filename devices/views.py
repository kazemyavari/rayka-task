from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DeviceSerializer


class DeviceCreateView(APIView):
    serializer_class = DeviceSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return Response(
            status=status.HTTP_201_CREATED,
            data={"message": "Item created successfully."},
        )
