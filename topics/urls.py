from django.urls import path
from topics.views import get_topics, get_one_topic

urlpatterns = [
    path('topics/', get_topics, name='topics'),
    path('onetopic/<str:pk>', get_one_topic, name='topic'),
]
