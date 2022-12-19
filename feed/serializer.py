from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from feed.models import Feed, Comments
from topics.serializers import TopicsSerializer
from users.models import Profile
from users.serializer import UserSerializer


class CommentatorSerializer(serializers.ModelSerializer):
    # user = UserSerializer(required=False, read_only=True)

    class Meta:
        model = Profile
        # fields = "__all__"
        fields = ["id", "avatar", "user", "following", "followedby", "bio", "followedby_count", "follow_count", 'my_posts_count']
        depth = 1


class CommentsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class FeedsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = "__all__"


class CommentsSerializer(serializers.ModelSerializer):
    # commentator = CommentatorSerializer(required=False, read_only=True)
    reply_count = SerializerMethodField()
    like_count = serializers.ReadOnlyField(required=False, read_only=True)

    class Meta:
        model = Comments
        fields = "__all__"
        depth = 1


    def get_fields(self):
        fields = super(CommentsSerializer, self).get_fields()
        fields['subcomments'] = CommentsSerializer(many=True)
        return fields

    @staticmethod
    def get_reply_count(obj):
        if obj.is_parent:
            return obj.children().count()
        return obj.subcomments.count()

    """
    A another way to get replies
    @staticmethod
    def get_parent(obj):
        if obj.parent is not None:
            return CommentsSerializer(obj.parent).data
        else:
            return None
    """


class FeedSerializer(serializers.ModelSerializer):
    # topic = TopicsSerializer(required=False, read_only=True)
    # profile = CommentatorSerializer(required=False, read_only=True)
    num_likes = serializers.ReadOnlyField(read_only=True, required=False)
    num_replies = serializers.ReadOnlyField(read_only=True, required=False)
    num_saves = serializers.ReadOnlyField(read_only=True, required=False)
    # replies = CommentsSerializer(many=True, read_only=True)

    # l_count = serializers.SerializerMethodField()
    # recent_post = serializers.SerializerMethodField()

    class Meta:
        model = Feed
        fields = '__all__'
        depth = 1

    """"ATTENTION!"""
    @staticmethod
    def get_replies(obj):
        # pro = Product.objects.select_related("category")
        return CommentsSerializer(obj.replies, many=True).data

    # @staticmethod
    # @property
    # def get_l_count(self, pk):
    #     comments = Comments.objects.filter(post=pk,)
    #         c= self.num_likes
    #     return c
