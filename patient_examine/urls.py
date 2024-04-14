from django.urls import path
from .views import *

urlpatterns = [
    path('patient/examine/', PatientExamineAPIView.as_view(), name='patient-examine')
]
