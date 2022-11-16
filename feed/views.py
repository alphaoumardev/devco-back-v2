from django.db.models import Q, Count
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import get_object_or_404, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from feed.models import Feed, Comments
from feed.serializer import FeedsPostSerializer, CommentsPostSerializer, FeedSerializer,  CommentsSerializer
from topics.models import Topics
from users.models import Profile


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def get_comments(request, pk):
    if request.method == 'GET':
        comments = Comments.objects.filter(post=pk, parent__comment=None)
        comment = CommentsSerializer(comments, many=True)
        return Response(comment.data)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def get_feeds(request):
    if request.method == 'GET':
        try:
            query = request.GET.get('query') if request.GET.get('query') is not None else ''
            feeds = Feed.objects.filter(
                Q(topic__name=query) |
                Q(title__contains=query) |
                Q(content__contains=query) |
                Q(title__exact=query)).order_by("-id")
            serializer = FeedSerializer(feeds, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)

    if request.method == 'POST':
        try:
            serializer = FeedsPostSerializer(data=request.data, many=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def get_one_feed(request, pk):
    if request.method == 'GET':
        # comments = Comments.objects.filter(post=pk)
        # comment = CommentsSerializer(comments, many=True)  # get comments of this post

        feed = Feed.objects.get(id=pk)
        feed.views += 1
        feed.save()
        serializer = FeedSerializer(feed, many=False)

        recent_posts = Feed.objects.filter(profile_id=feed.profile_id).order_by('id').exclude(id=feed.id).reverse()[:3]
        recent_p_seriliazer = FeedSerializer(recent_posts, many=True)
        """To Jenny"""
        print('\n'.join
              ([''.join
                ([('Jenny'[(x - y) % 5]
                   if ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1)
                      ** 3 - (x * 0.05) ** 2 * (y * 0.1)
                      ** 3 <= 0 else ' ')
                  for x in range(-30, 30)])
                for y in range(15, -15, -1)]))

        return Response({"data": serializer.data,
                         # "comments": comments.data,
                         "recent_posts": recent_p_seriliazer.data
                         })

    if request.method == "POST":  # to reply
        try:
            serializer = CommentsPostSerializer(data=request.data, many=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def edit_my_posts(request, pk):
    feed = Feed.objects.get(id=pk, profile__user_id=request.user.id)
    if request.method == "PATCH":
        try:
            serializer = FeedsPostSerializer(feed, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)

    if request.method == "DELETE":
        try:
            feed.delete()
            return Response(
                {"message": "You have successfully deleted your devco account and hope you will return soon",
                 "status": status.HTTP_204_NO_CONTENT})
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_feed_by_topic(request, pk):
    if request.method == 'GET':
        try:
            topic = Topics.objects.get(name=pk)
            feed = Feed.objects.filter(topic=topic)
            serializer = FeedSerializer(feed, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like_one_feed(request, pk):
    current_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        try:
            likes_post = get_object_or_404(Feed, id=pk)
            if likes_post.likes.filter(user_id=request.user.id).exists():
                likes_post.likes.remove(current_profile)
                likes_post.save()
                return Response("unliked")

            else:
                likes_post.likes.add(current_profile)
                likes_post.save()
                return Response("liked")
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_one_feed(request, pk):
    if request.method == "POST":
        try:
            current_profile = Profile.objects.get(user=request.user)
            saves_post = get_object_or_404(Feed, id=pk)
            if saves_post.saves.filter(user_id=request.user.id).exists():
                saves_post.saves.remove(current_profile)
                saves_post.save()
                return Response("unsaved")

            else:
                saves_post.saves.add(current_profile)
                saves_post.save()
                return Response("liked")
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_trending_feed(request):
    if request.method == 'GET':
        try:
            feed = Feed.objects.annotate(Count('views')).order_by('-views')[:4]
            serializer = FeedSerializer(feed, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)
