from django.db.models import Count
from django.urls import path
from rest_framework.generics import ListAPIView

from feed.models import Feed
from feed.serializer import FeedCountSerializer
from feed.views import get_feeds, get_feed_by_topic, like_one_feed, get_one_feed, save_one_feed, CreatePost, \
     get_trending_feed

urlpatterns = [
    path('feeds/', get_feeds, name='feeds'),
    path('feed/<str:pk>', get_one_feed, name='feed'),
    path('feedbytopic/<str:pk>', get_feed_by_topic, name='feedbytopic'),
    path('likes/<str:pk>', like_one_feed, name='likes'),
    path('saves/<str:pk>', save_one_feed, name='saves'),
    path('creat/', CreatePost.as_view(), name='creat'),
    path('trending/', get_trending_feed, name='trending'),

    path('count/', ListAPIView.as_view(
        queryset=Feed.objects.all().annotate(topic_count=Count("topic")).order_by('topic__name'),
        serializer_class=FeedCountSerializer),
        name="num"
    )
]
