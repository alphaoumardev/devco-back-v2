from django.db.models import Q, Count
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from feed.models import Feed
from feed.serializer import FeedsSerializer, RepliePostSerializer, FeedSerializer
from feed.models import Replies
from feed.serializer import ReplieSerializer
from topics.models import Topics


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def get_feeds(request):
    if request.method == 'GET':
        query = request.GET.get('query') if request.GET.get('query') is not None else ''
        feeds = Feed.objects.filter(
            Q(topic__name=query) | Q(title__contains=query) | Q(content__contains=query) |
            Q(title__exact=query)).order_by("-id")
        serializer = FeedSerializer(feeds, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = FeedsSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class CreatePost(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @staticmethod
    def post(request):
        serializer = FeedsSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def get_one_feed(request, pk):
    if request.method == 'GET':
        comments = Replies.objects.filter(post=pk)
        comment = ReplieSerializer(comments, many=True)  # get comments of this post

        feed = Feed.objects.get(id=pk)
        feed.views += 1
        feed.save()
        serializer = FeedSerializer(feed, many=False)
        return Response({"data": serializer.data, "comments": comment.data})

    if request.method == "POST":  # to reply
        likes = get_object_or_404(Feed, id=pk)
        likes.likes.add(request.user)
        serializer = RepliePostSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def get_feed_by_topic(request, pk):
    if request.method == 'GET':
        topic = Topics.objects.get(name=pk)
        feed = Feed.objects.filter(topic=topic)
        serializer = FeedSerializer(feed, many=True)
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like_one_feed(request, pk):
    if request.method == "POST":
        likes_post = get_object_or_404(Feed, id=pk)
        if likes_post.likes.filter(id=request.user.id).exists():
            likes_post.likes.remove(request.user)
            likes_post.save()
            return Response("unliked")

        else:
            likes_post.likes.add(request.user)
            likes_post.save()
            return Response("liked")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_one_feed(request, pk):
    if request.method == "POST":
        saves_post = get_object_or_404(Feed, id=pk)
        if saves_post.saves.filter(id=request.user.id).exists():
            saves_post.saves.remove(request.user)
            saves_post.save()
            return Response("unsaved")

        else:
            saves_post.saves.add(request.user)
            saves_post.save()
            return Response("liked")


@api_view(["GET"])
@permission_classes([AllowAny])
def get_trending_feed(request):
    if request.method == 'GET':
        feed = Feed.objects.annotate(Count('views')).order_by('-views')[:4]
        serializer = FeedSerializer(feed, many=True)
        return Response(serializer.data)
