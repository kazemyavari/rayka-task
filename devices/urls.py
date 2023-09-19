from django.urls import path, re_path
from .views import DeviceCreateView


urlpatterns = [
    path("", DeviceCreateView.as_view(), name="create_device"),
]
