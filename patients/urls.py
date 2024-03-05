from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patients')

urlpatterns = []

urlpatterns = urlpatterns + router.urls
