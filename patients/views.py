from django.http import Http404
from django.utils.translation import gettext_lazy as _

from rest_framework import viewsets, mixins, status, exceptions, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from utils.mixins import PaginationMixin
from utils.paginations import FetusPageNumberPagination
from users.auth import UserTokenAuthentication
from models import Patient

class PatientViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    PaginationMixin,
):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = FetusPageNumberPagination
    authentication_classes = [UserTokenAuthentication]
    queryset = Patient.objects.all()

    class UserException(exceptions.APIException):
        status_code = status.HTTP_403_FORBIDDEN
        default_detail = {
            'response_code': status.HTTP_403_FORBIDDEN,
            'response_message': _('User with provided token/id is not valid.'),
            'data': None
        }
        default_code = 'invalid_user'

    def list(self, request):
        """
        API to list all patients

        ### Example Request:
            GET /api/patients/
        ### Example Response:
        {
            "response_code": 200,
            "data": {
                "count": 10,
                "next": "http://127.0.0.1:8000/api/patients/?page=2",
                "prev": null,
                "results": [
                    {
                        "id": 24,
                        "first_name": "MitraTest2",
                        "last_name": "Test2",
                        "email": "test2@gmail.com",
                        "phone_number": "004928166432",
                        "profile_image": null,
                    },.....
                ],
            },
            "response_message": "User details sent successfully."
        }
        """

        try:
            _ = get_object_or_404(Patient, pk=request.user.id)
            page = self.paginate_queryset(self.queryset)
            if page is not None:
                serializer = self.get_paginated_response(
                    self.get_serializer(page, many=True).data
                )
            else:
                serializer = self.get_serializer(self.queryset, many=True)
            return Response({
                    'response_code': status.HTTP_200_OK,
                    'data': serializer.data,
                    'response_message': _('User details sent successfully.')
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return self.handle_exceptions(e, 'No user details found.')


    def handle_exceptions(self, e, message):
        if isinstance(e, Http404):
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'data': None,
                'response_message': _(message),
            }, status=status.HTTP_404_NOT_FOUND)
        if isinstance(e, PatientViewSet.UserException):
            return Response(
                e.default_detail,
                status=e.status_code
            )
        else:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'data': None,
                'response_message': _('Something went wrong. Please try again later.'),
            }, status=status.HTTP_400_BAD_REQUEST)
