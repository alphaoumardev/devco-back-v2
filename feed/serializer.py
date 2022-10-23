from rest_framework import serializers
from feed.models import Feed, Replies
from topics.serializers import TopicsSerializer
from users.serializer import UserSerializer


class FeedsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = "__all__"


class FeedSerializer(serializers.ModelSerializer):
    topic = TopicsSerializer(required=False, read_only=True)
    user = UserSerializer(required=False, read_only=True)
    num_likes = serializers.ReadOnlyField(read_only=True, required=False)
    num_replies = serializers.ReadOnlyField(read_only=True, required=False)
    num_saves = serializers.ReadOnlyField(read_only=True, required=False)

    class Meta:
        model = Feed
        fields = '__all__'

    # @property
    # def get_lik(self, obj):
    #     liked_post = get_object_or_404(Feed, id=obj.user)
    #
    #     if liked_post.likes.filter(related_like__user=obj.user.id).exists():
    #         print(self.user)
    #         return True
    #     else:
    #         return False


class FeedCountSerializer(serializers.ModelSerializer):
    topic = TopicsSerializer(required=False, read_only=True)
    topic_count = serializers.IntegerField()

    def get_topic_count(self, obj):
        return obj.topic_count.count()

    class Meta:
        model = Feed
        fields = '__all__'


class ReplieSerializer(serializers.ModelSerializer):
    commentator = UserSerializer(required=False, read_only=True)

    class Meta:
        model = Replies
        fields = '__all__'


class RepliePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Replies
        fields = '__all__'
