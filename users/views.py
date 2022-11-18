from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Count
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from feed.models import Feed
from feed.serializer import FeedSerializer
from .models import Profile
from .serializer import UserSerializer, RegisterSerializer, ChangePasswordSerializer, ProfileSerializer, \
    ProfilePostSerializer


class RegisterAPI(generics.GenericAPIView):  # Register API
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        email = data.get('email')
        serializer = self.get_serializer(data=data)
        users_qs = User.objects.filter(email=email)
        user_name = User.objects.filter(username=username)
        if users_qs.exists():
            return Response({'A user with this email already exists'})
        elif user_name.exists():
            return Response({'A user with this username already exists'})
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            Profile.objects.create(user=user)  # To create automatically a profile during registering
        except Exception as e:
            return Response({'detail': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, formats=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class ChangePasswordView(generics.UpdateAPIView):  # To change the password
    serializer_class = ChangePasswordSerializer  # An endpoint for changing password.
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):  # Check old password
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))  # set_password hashes the password
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


@api_view(["GET", "POST", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def get_my_profile(request):
    current_profile = Profile.objects.get(user=request.user)

    if request.method == 'GET':
        serializer = ProfileSerializer(current_profile, many=False)
        """To get my posts"""
        my_feed = Feed.objects.filter(profile__user=request.user).order_by('id').reverse()
        mine = FeedSerializer(my_feed, many=True)

        """To get my followers"""
        followedby = current_profile.followedby.all()
        followedby_serializer = ProfileSerializer(followedby, many=True)

        """To get my following"""
        following = current_profile.following.all()
        following_serializer = ProfileSerializer(following, many=True)

        """To get liked posts"""
        liked_posts = Feed.objects.filter(likes=current_profile)
        liked_serializer = FeedSerializer(liked_posts, many=True)

        """To get saved posts"""
        saved_posts = Feed.objects.filter(saves=current_profile)
        saved_serializer = FeedSerializer(saved_posts, many=True)

        return Response({
            "data": serializer.data,
            "my_posts": mine.data,
            "followedby": followedby_serializer.data,
            "following": following_serializer.data,
            "liked_posts": liked_serializer.data,
            "saved_posts": saved_serializer.data,
        })

    if request.method == "POST":
        try:
            serializer = ProfilePostSerializer(data=request.data, many=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors)
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)

    if request.method == "PATCH":
        try:
            profile = Profile.objects.get(user_id=request.user.id)
            the_user = User.objects.get(id=profile.user.id)
            serializer = ProfilePostSerializer(profile, data=request.data)
            if serializer.is_valid():
                """To update the user simultaneously"""
                new_user = UserSerializer(the_user, data=request.data)
                if new_user.is_valid():
                    new_user.save()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors)
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)

    if request.method == "DELETE":
        try:
            profile = Profile.objects.get(user_id=request.user.id)
            profile.delete()
            return Response(
                {"message": "You have successfully deleted your devco account and hope you will return soon",
                 "status": status.HTTP_204_NO_CONTENT})
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_his_profile(request, pk):
    if request.method == 'GET':
        try:
            profile = Profile.objects.get(id=pk)
            his_feed = Feed.objects.filter(profile_id=pk)
            """to get his profile and posts"""
            his_posts = FeedSerializer(his_feed, many=True)
            serializer = ProfileSerializer(profile, many=False)
            """to get his followers"""
            followedby = profile.followedby.all()
            by_serializer = ProfileSerializer(followedby, many=True)
            """to get his following"""
            following = profile.following.all()
            following_serializer = ProfileSerializer(following, many=True)

            return Response({
                "data": serializer.data,
                "hisposts": his_posts.data,
                "hisfollowers": by_serializer.data,
                "hisfollowing": following_serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def i_follow_profile(request, pk):
    pass
    if request.method == "POST":
        try:
            current_profile = Profile.objects.get(user=request.user)
            profile_to_follow = Profile.objects.get(id=pk)
            # current_profile.following.remove(profile_to_follow)
            # current_profile.followedby.remove(profile_to_follow)

            # profile_to_follow.followedby.remove(current_profile)
            # profile_to_follow.following.remove(current_profile)
            # current_profile.save()
            # profile_to_follow.save()
            # return Response('Y')

            if current_profile == profile_to_follow:
                return Response("You cannot follow youserlf")
            if profile_to_follow in current_profile.following.all():
                current_profile.following.remove(profile_to_follow)
                current_profile.save()

                profile_to_follow.followedby.remove(current_profile)
                profile_to_follow.save()
                return Response('Unfollowed this profile')

            else:
                current_profile.following.add(profile_to_follow)
                current_profile.save()

                profile_to_follow.followedby.add(current_profile)
                profile_to_follow.save()

                return Response('Followed this profile')
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profiles_following_me(request):
    if request.method == "GET":
        try:
            current_profile = Profile.objects.get(user=request.user)
            followedby = current_profile.followedby.all()
            serializer = ProfileSerializer(followedby, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profiles_i_follow(request):
    if request.method == "GET":
        try:
            current_profile = Profile.objects.get(user=request.user)
            following = current_profile.following.all()
            serializer = ProfileSerializer(following, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile_to_follow(request):
    if request.method == "GET":
        try:
            profiles = Profile.objects.get(user=request.user)
            following = profiles.following.all()
            """recommand profiles to follow"""
            profile_to_follow = Profile.objects \
                                    .annotate(following_count=Count('following')).order_by('following_count') \
                                    .reverse().exclude(user=request.user) \
                                    .exclude(profile__following__in=following)
            serializer = ProfileSerializer(profile_to_follow, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def posts_i_liked(request):
    if request.method == "GET":
        try:
            current_profile = Profile.objects.get(user_id=request.user.id)
            liked_posts = Feed.objects.filter(likes=current_profile)
            serializer = FeedSerializer(liked_posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def posts_i_saved(request):
    if request.method == "GET":
        try:
            current_profile = Profile.objects.get(user_id=request.user.id)
            saved_posts = Feed.objects.filter(saves=current_profile)
            serializer = FeedSerializer(saved_posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)
