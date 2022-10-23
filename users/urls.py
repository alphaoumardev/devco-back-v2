from .views import RegisterAPI, UserAPI, ChangePasswordView, get_profile
from knox import views as knox_views
from .views import LoginAPI
from django.urls import path

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('profile/', get_profile, name='profile'),

    path('loaduser/', UserAPI.as_view()),
]
