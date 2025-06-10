from django.urls import path
from .views import RegisterView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserMeView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserMeView.as_view(), name='user-me'),
]
