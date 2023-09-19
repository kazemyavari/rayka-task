from django.urls import path, re_path
from .views import DeviceCreateView, DeviceRetrieveView


urlpatterns = [
    path("", DeviceCreateView.as_view(), name="create_device"),
    path("id<pk>/", DeviceRetrieveView.as_view(), name="get_device"),
]
