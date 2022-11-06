from rest_framework import serializers
from django.contrib.auth.models import User

from users.models import Profile


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        users_qs = User.objects.filter(email=data['email'])
        user_name = User.objects.filter(username=['username'])
        if users_qs.exists() or user_name.exists():
            raise serializers.ValidationError('A user with this email or username already exists')
        else:
            return data

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        validated_data['email'],
                                        validated_data['password'], )
        return user


# Serializer for password change endpoint.
class ChangePasswordSerializer(serializers.Serializer, ):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False, read_only=True)
    my_posts_count = serializers.ReadOnlyField(read_only=True, required=False)
    my_followers_count = serializers.ReadOnlyField(read_only=True, required=False)
    my_following_count = serializers.ReadOnlyField(read_only=True, required=False)

    class Meta:
        model = Profile
        fields = '__all__'


class ProfilePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
