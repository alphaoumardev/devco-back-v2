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


@api_view(["GET", "POST", "PATCHT", "DELETE"])
@permission_classes([IsAuthenticated])
def get_my_profile(request):
    profile = Profile.objects.get(user_id=request.user.id)

    if request.method == 'GET':
        my_feed = Feed.objects.filter(profile__user_id=request.user.id).order_by('id').reverse()
        mine = FeedSerializer(my_feed, many=True)
        serializer = ProfileSerializer(profile, many=False)
        return Response({"data": serializer.data, "my_posts": mine.data})

    if request.method == "POST":
        try:
            serializer = ProfilePostSerializer(data=request.data, many=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors)
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)

    if request.method == "PATCHT":
        try:
            serializer = ProfilePostSerializer(profile, data=request.data)
            if serializer.is_valid():
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
            profile = Profile.objects.get(user_id=pk)
            my_feed = Feed.objects.filter(profile__user_id=pk)
            mine = FeedSerializer(my_feed, many=True)
            serializer = ProfileSerializer(profile, many=False)
            return Response({"data": serializer.data, "hispost": mine.data})
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def i_follow_profile(request, pk):
    if request.method == "POST":
        try:
            current_profile = Profile.objects.get(user_id=request.user.id)
            other_profiles = Profile.objects.get(user_id=pk)

            if current_profile == other_profiles:
                return Response("You cannot follow youserlf")
            if other_profiles in current_profile.followers.all():
                current_profile.followers.remove(other_profiles)
                current_profile.save()
                return Response('Unfollowed this profile')

            else:
                current_profile.followers.add(other_profiles)
                current_profile.save()
                return Response('Followed this profile')
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profiles_following_me(request):
    if request.method == "GET":
        try:
            current_profile = Profile.objects.get(user_id=request.user.id)
            for following in current_profile.followers.all():
                fo = following.followers.all()
                serializer = ProfileSerializer(fo, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profiles_i_follow(request):
    if request.method == "GET":
        try:
            current_profile = Profile.objects.get(user_id=request.user.id)
            followers = current_profile.followers.all()
            serializer = ProfileSerializer(followers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile_to_follow(request):
    if request.method == "GET":
        try:
            profile_to_follow = Profile.objects.annotate(followers_count=Count('followers')) \
                                    .order_by('followers_count').reverse().exclude(user=request.user)[:3]
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
