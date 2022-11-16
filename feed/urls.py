from django.urls import path
from feed.views import get_feeds, get_feed_by_topic, like_one_feed, get_one_feed, save_one_feed, get_trending_feed, \
    edit_my_posts, get_comments

urlpatterns = [
    path('feeds/', get_feeds, name='feeds'),
    path('feed/<str:pk>', get_one_feed, name='feed'),
    path('feedbytopic/<str:pk>', get_feed_by_topic, name='feedbytopic'),
    path('likes/<str:pk>', like_one_feed, name='likes'),
    path('saves/<str:pk>', save_one_feed, name='saves'),
    path('trending/', get_trending_feed, name='trending'),

    path('com/<pk>', get_comments, name="com"),
    path('edit-my-post/<str:pk>', edit_my_posts, name='edit-my-post'),
]
