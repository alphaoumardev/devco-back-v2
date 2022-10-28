from .views import RegisterAPI, UserAPI, ChangePasswordView, get_my_profile, get_his_profile, i_follow_profile, \
    profile_follow_me, get_profile_to_follow
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
    path('his-profile/<str:pk>', get_his_profile, name='profile'),
    path('follow/<str:pk>', i_follow_profile, name='profile'),
    path('following-me/', profile_follow_me, name="following-me"),
    path('recommanded-profiles/', get_profile_to_follow, name="recommaded-profiles"),
    path('loaduser/', UserAPI.as_view()),
]
