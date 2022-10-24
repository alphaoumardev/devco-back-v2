from django.contrib.auth import login
from django.contrib.auth.models import User
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from feed.models import Feed
from feed.serializer import FeedSerializer
from .models import Profile
from .serializer import UserSerializer, RegisterSerializer, ChangePasswordSerializer, ProfileSerializer, \
    ProfilePostSerializer


# Register API
class RegisterAPI(generics.GenericAPIView):
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
        if user_name.exists():
            return Response({'A user with this username already exists'})

        # else:
        #     return data
        # if User.objects.filter(email=email).exists():
        #     messages['errors'].append("Account already exists with this email id.")
        # if User.objects.filter(username__iexact=username).exists():
        #     messages['errors'].append("Account already exists with this username.")
        # if len(messages['errors']) > 0:
        #     return Response({"detail": messages['errors']}, status=status.HTTP_400_BAD_REQUEST)
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
        profile = Profile.objects.get(user_id=request.user.id)
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
        current_profile = Profile.objects.get(user_id=request.user.id)
        profile_to_follow = Profile.objects.get(user_id=pk)
        print(current_profile, profile_to_follow)

        if current_profile == profile_to_follow:
            return Response("You cannot follow youserlf")
        if profile_to_follow in current_profile.followers.all():
            current_profile.followers.remove(profile_to_follow)
            current_profile.save()
            return Response('unfollowed')

        else:
            current_profile.followers.add(profile_to_follow)
            current_profile.save()
            return Response('followed')


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def i_follow_users(request, pk):
    if request.method == "POST":
        # profile_to_follow = get_object_or_404(Profile, user_id=pk)
        # follows = Profile.objects.all().exclude(user_id=request.user.id)

        profile_to_follow = Profile.objects.get(user_id=pk)
        currentUser = Profile.objects.get(user_id=request.user.id)
        my_following_users = profile_to_follow.followers.all()

        if pk != currentUser.user_id:
            if currentUser in my_following_users:
                profile_to_follow.followers.remove(currentUser.id)

                return Response('unfollowed')

            else:
                profile_to_follow.followers.add(currentUser.user_id)
                return Response('followed')
