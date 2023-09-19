from rest_framework import serializers
from rest_framework.serializers import Serializer
from .models import Devices


class DeviceSerializer(Serializer):
    __model__ = Devices()

    id = serializers.CharField(max_length=50, allow_null=False)
    deviceModel = serializers.CharField(max_length=100, allow_null=False)
    name = serializers.CharField(max_length=200, allow_null=False)
    note = serializers.CharField(max_length=1000, allow_null=False)
    serial = serializers.CharField(max_length=100, allow_null=False)

    def validate_deviceModel(self, value):
        device_model = value.replace("/devicemodels/id", "")

        if not device_model.isdigit():
            raise serializers.ValidationError(
                "deviceModel field must be in this format /devicemodels/id<int>"
            )

        return value

    def validate_id(self, value):
        id = value.replace("/devices/id", "")

        if not id.isdigit():
            raise serializers.ValidationError(
                "id field must be in this format: /devices/id<pk>"
            )
        device_item = self.__model__.table.get_item(Key={"id": value})
        if "Item" in device_item:
            raise serializers.ValidationError(
                f"Item already exists with this id: {value}."
            )

        return value

    def save(self, **kwself):
        self.__model__.table.put_item(Item=self.validated_data)
