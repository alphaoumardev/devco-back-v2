from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import *


class TopicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = "__all__"


class TopicsCountSerializer(serializers.ModelSerializer):
    post_count = SerializerMethodField()

    def get_post_count(self, obj):
        return obj.post_count

    class Meta:
        model = Topics
        fields = "__all__"
