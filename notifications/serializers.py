from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from notifications.models import Notifications
from feed.serializer import CommentatorSerializer, FeedSerializer, CommentsSerializer


class NotificationSerializer(serializers.ModelSerializer):
    from_profile = serializers.SerializerMethodField(read_only=True, required=False)
    to_profile = serializers.SerializerMethodField(read_only=True, required=False)
    new_post = serializers.SerializerMethodField(read_only=True, required=False)
    new_follower = serializers.SerializerMethodField(read_only=True, required=False)

    class Meta:
        model = Notifications
        fields = '__all__'

    @staticmethod
    def get_from_profile(obj):
        return CommentatorSerializer(obj.from_profile, many=False).data

    @staticmethod
    def get_to_profile(obj):
        return CommentatorSerializer(obj.to_profile, many=False).data

    @staticmethod
    def get_new_post(obj):
        return FeedSerializer(obj.new_post, many=False).data

    @staticmethod
    def get_new_follower(obj):
        return CommentatorSerializer(obj.new_follower, many=False).data
