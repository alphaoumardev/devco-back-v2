from .views import RegisterAPI, UserAPI, ChangePasswordView, get_my_profile, get_his_profile, i_follow_profile, \
    profiles_i_follow, get_profile_to_follow, posts_i_liked, posts_i_saved, profiles_following_me
from knox import views as knox_views
from .views import LoginAPI
from django.urls import path

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    path('my-profile/', get_my_profile, name='profile'),
    path('follow/<str:pk>', i_follow_profile, name='profile'),
    path('followedby/', profiles_following_me, name="i_follow"),
    path('i-follow/', profiles_i_follow, name="following-me"),
    path('recommanded-profiles/', get_profile_to_follow, name="recommaded-profiles"),
    path('my-likes/', posts_i_liked, name="liked_posts"),
    path('my-savings/', posts_i_saved, name="saved_posts"),

    path('his-profile/<str:pk>', get_his_profile, name='profile'),

    path('loaduser/', UserAPI.as_view()),
]
