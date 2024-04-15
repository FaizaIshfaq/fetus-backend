from django.utils.translation import gettext_lazy as _

from rest_framework import status, permissions, generics, filters
from rest_framework.response import Response

from utils.exceptions import (
    handle_exceptions
)
from users.auth import UserTokenAuthentication

from .models import Doctor
from .serializers import DoctorSerializer


class DoctorAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [UserTokenAuthentication]
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def list(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(
                self.filter_queryset(
                    self.get_queryset()
                )[:5], many=True)

            return Response({
                    'response_code': status.HTTP_200_OK,
                    'data': serializer.data,
                    'response_message': _('Doctor details sent successfully.')
                }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return handle_exceptions(e, 'No doctor details found.')
