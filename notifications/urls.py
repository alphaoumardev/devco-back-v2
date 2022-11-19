from django.urls import path
from notifications.views import get_notifications, delete_notification

urlpatterns = [
    path('notifications/', get_notifications, name="notifications"),
    path('read/<str:pk>', delete_notification, name="read_notification")
]
