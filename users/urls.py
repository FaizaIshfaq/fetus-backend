from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('auth-token/', AuthTokenView.as_view(), name='auth_token')
]

urlpatterns = urlpatterns + router.urls
