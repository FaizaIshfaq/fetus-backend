from django.urls import path
from .views import *

urlpatterns = [
    path('patient/<int:id>/femur-examine/', PatientFemurExamineAPIView.as_view(), name='patient-femur-examine'),
    path('patient/<int:id>/head-examine/', PatientHeadExamineAPIView.as_view(), name='patient-head-examine')
]
