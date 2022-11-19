from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from notifications.models import Notifications
from notifications.serializers import NotificationSerializer
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from django.db.models import Q, Count
from rest_framework import status
from rest_framework.generics import get_object_or_404, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import Profile
from feed.models import Feed


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_notifications(request, ):
    current_profile = Profile.objects.get(user=request.user)

    if request.method == 'GET':
        try:
            notifications = Notifications.objects.filter(to_profile=current_profile).order_by('id').reverse()
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_notification(request, pk):
    current_profile = Profile.objects.get(user=request.user)
    notification = Notifications.objects.get(to_profile=current_profile, id=pk)
    if request.method == 'DELETE':
        try:
            notification.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)
