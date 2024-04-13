from django.urls import path

from .views import *

urlpatterns = [
    path('doctors/', DoctorAPIView.as_view(), name='all-doctors')
]
