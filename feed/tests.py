from rest_framework.authtoken.admin import User
import numpy as np

from feed.models import Feed


# Create your tests here.
def trendingpostfunction():
    rdata = Feed.objects.filter()
    likerate = []
    dislikerate = []
    viewrate = []
    for i in rdata:
        lr = i.post_like.count() + 1
        vr = i.post_views + 1
        lr = lr / vr
        likerate.append(lr)
        dr = i.post_dislike.count() + 1
        dr = dr / vr
        dislikerate.append(dr)
        u = User.objects.count()
        vrt = vr / u
        viewrate.append(vrt)
    lr1 = np.array(likerate)
    dr1 = np.array(dislikerate)
    vr1 = np.array(viewrate)
    lr = lr1.round(2)
    dr = dr1.round(2)
    vr = vr1.round(2)
    results = []
    for i in lr, dr, vr:
        a = (lr - dr) + vr
        a = a * 50
    rdata = Feed.objects.filter()
    trendingdata = a
    j = 0
    trendingdict = {}
    for i in rdata:
        trendingdict[i.id] = trendingdata[j]
        j += 1
    trend = {k: v for k, v in sorted(trendingdict.items(), key=lambda item: item[1],
                                     reverse=True)}
    print('latest trending --', trend)
    trendlist = []
    for k in trend.keys():
        trendlist.append(k)
    # print('trendlist --', trendlist)
    return trendlist


"""
class CommentsSerializer(serializers.ModelSerializer):
    commentator = ProfileSerializer(required=False, read_only=True)

    class Meta:
        model = Comments
        fields = '__all__'
        depth = 3


class CommentSerializer(serializers.ModelSerializer):
    reply_count = SerializerMethodField()

    class Meta:
        model = Comments
        fields = "__all__"
        # fields = [
        #     'id',
        #     'post',
        #     'commentator',
        #     'parent',
        #     'comment',
        #     'reply_count',
        #     'liking',
        #     'commentated',
        # ]

    @staticmethod
    def get_reply_count(obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = [
            'id',
            'parent',
            'commentator',
            'comment',
            'timestamp',
        ]


class CommentDetailSerializer(serializers.ModelSerializer):
    reply_count = SerializerMethodField()
    replie = SerializerMethodField()

    class Meta:
        model = Comments
        fields = [
            'id',
            'post',
            'parent',
            'commentator',
            'comment',
            'timestamp',
            'reply_count',
            'replie',
        ]

    @staticmethod
    def get_replie(obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    @staticmethod
    def get_reply_count(obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

"""