from knox.models import AuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404

from feed.models import Feed
from feed.serializer import FeedSerializer
from .models import Profile
from .serializer import UserSerializer, RegisterSerializer, ChangePasswordSerializer, ProfileSerializer, \
    ProfilePostSerializer
from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


# To change the password
class ChangePasswordView(generics.UpdateAPIView):
    # An endpoint for changing password.
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
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


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def get_profile(request):
    if request.method == 'GET':
        profile = Profile.objects.get(id=request.user.id)
        my_p = Feed.objects.filter(user_id=request.user.id)
        my = FeedSerializer(my_p, many=True)
        serializer = ProfileSerializer(profile, many=False)
        return Response({"data": serializer.data, "mypost": my.data})

    if request.method == "POST":
        serializer = ProfilePostSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def users_following_me(request, pk):
    if request.method == "POST":
        # the_user_to_follow = get_object_or_404(Profile, user_id=pk)
        # follows = Profile.objects.all().exclude(user_id=request.user.id)

        the_user_to_follow = Profile.objects.get(user_id=pk)
        currentUser = Profile.objects.get(user_id=request.user.id)
        my_following_users = the_user_to_follow.followers.all()

        if pk != currentUser.user_id:
            if currentUser in my_following_users:
                the_user_to_follow.followers.remove(currentUser.id)

                return Response('unfollowed')

            else:
                the_user_to_follow.followers.add(currentUser.user_id)
                return Response('followed')


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def i_follow_users(request, pk):
    if request.method == "POST":
        # the_user_to_follow = get_object_or_404(Profile, user_id=pk)
        # follows = Profile.objects.all().exclude(user_id=request.user.id)

        the_user_to_follow = Profile.objects.get(user_id=pk)
        currentUser = Profile.objects.get(user_id=request.user.id)
        my_following_users = the_user_to_follow.followers.all()

        if pk != currentUser.user_id:
            if currentUser in my_following_users:
                the_user_to_follow.followers.remove(currentUser.id)

                return Response('unfollowed')

            else:
                the_user_to_follow.followers.add(currentUser.user_id)
                return Response('followed')
