from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patients')

urlpatterns = [
    path('patient/appointments/', PatientAppointmentsAPIView.as_view(), name='patient-appointments'),
    path('patient/records/', PatientRecordsAPIView.as_view(), name='patient-records')
]

urlpatterns = urlpatterns + router.urls
