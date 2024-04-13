from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patients')

urlpatterns = [
    path('patients/appointments/', PatientAppointmentsAPIView.as_view(), name='patient-appointments')
]

urlpatterns = urlpatterns + router.urls
