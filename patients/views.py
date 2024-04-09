from django.utils.translation import gettext_lazy as _

from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, mixins, status, permissions
from rest_framework.response import Response

from utils.mixins import PaginationMixin
from utils.paginations import FetusPageNumberPagination
from utils.exceptions import (
    UserException,
    handle_exceptions
)
from users.auth import UserTokenAuthentication
from .models import Patient
from .serializers import PatientSerializer


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
    serializer_class = PatientSerializer
    queryset = Patient.objects.filter(is_active=True).order_by('id')

    def list(self, request):
        """
        API to list all patients

        ### Example Request:
            GET /api/patients/
        ### Example Response:
        {
            "response_code": 200,
            "data": {
                "total_pages": 1,
                "count": 1,
                "next": null,
                "previous": null,
                "results": [
                    {
                        "id": 1,
                        "first_name": "Martin",
                        "last_name": "Alex",
                        "date_of_birth": "1972-09-25",
                        "gender": "m",
                        "examine_date": "2024-03-30",
                        "trimester": "1",
                        "blood_group": "O+",
                        "age": 52,
                        "examine_by": "doctor",
                        "email": "example@example.com",
                        "phone_number": "123456789",
                        "profile_image": null,
                        "is_active": true
                    }
                ]
            },
            "response_message": "User details sent successfully."
        }
        """

        try:
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
            print(e)
            return handle_exceptions(e, 'No patients details found.')

    def create(self, request, *args, **kwargs):
        """
        API to create patient

        ### Example Request:
            POST /api/patients/
            {
                "first_name": "f",
                "last_name": "i",
                "date_of_birth": "2001-10-20",
                "gender": "f",
                "examine_date": "2024-6-06",
                "trimester": "2",
                "blood_group": "O+",
                "age": 21,
                "examine_by": "Doctor",
                "phone_number": "92302240912"
            }
        ### Example Response:
        {
            "response_code": 201,
            "response_message": "Patient created successfully.",
            "data": {
                "patient": {
                    "id": 8,
                    "first_name": "f",
                    "last_name": "i",
                    "date_of_birth": "2001-10-20",
                    "gender": "f",
                    "examine_date": "2024-06-06",
                    "trimester": "2",
                    "blood_group": "O+",
                    "age": 21,
                    "examine_by": "Doctor",
                    "email": null,
                    "phone_number": "92302240912",
                    "profile_image": null,
                    "is_active": true
                }
            }
        }
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            payload = serializer.data

            patient = Patient.objects.filter(phone_number=payload.get("phone_number"))
            if patient:
                return Response({
                    "response_code": status.HTTP_200_OK,
                    "response_message": _('Patient with this phone already exist.'),
                    "data": None,
                }, status=status.HTTP_200_OK)

            patient = Patient.objects.create(
                first_name=payload.get('first_name'),
                last_name=payload.get('last_name'),
                date_of_birth=payload.get('date_of_birth'),
                gender=payload.get('gender'),
                examine_date=payload.get('examine_date'),
                trimester=payload.get('trimester'),
                blood_group=payload.get('blood_group'),
                age=payload.get('age'),
                examine_by=payload.get('examine_by'),
                phone_number=payload.get('phone_number'),
            )
            if payload.get('email'):
                patient.email = payload.get('email')

            patient.save()

            return Response({
                "response_code": status.HTTP_201_CREATED,
                "response_message": _('Patient created successfully.'),
                "data": {
                    'patient': self.serializer_class(patient).data,
                },
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return handle_exceptions(e, 'Unable to create patient.')

    def update(self, request, *args, **kwargs):
        """
        API to update Patient fields

        ### Example Request:
            PUT /api/patients/<patient_id>/
            {
                "first_name": "Mitra",
                "last_name": "Home",
                "phone_number": "004912225922",
                "email": "test123@example.com".
                "profile_image": 'image_to_upload.png',
            }
        ### Example Response:
            {
                "response_code": 200,
                "data": {
                    "id": 1,
                    "first_name": "Martin",
                    "last_name": "Alex",
                    "date_of_birth": "1972-09-25",
                    "gender": "m",
                    "examine_date": "2024-03-30",
                    "trimester": "1",
                    "blood_group": "O+",
                    "age": 52,
                    "examine_by": "doctor",
                    "email": "example@example.com",
                    "phone_number": "123456789",
                    "profile_image": null,
                    "is_active": true
                },
                "response_message": "Patient updated successfully."
            }
        """

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response({
                    'response_code': status.HTTP_200_OK,
                    'data': serializer.data,
                    'response_message': _('Patient updated successfully.'),
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return handle_exceptions(e, 'Patient does not exist.')

    def retrieve(self, request, *args, **kwargs):
        """
        API to retrieve details of a single Patient.

        ### Example Request:
            GET /api/patients/<patient_id>/
        ### Example Response:
        {
            "response_code": 200,
            "data": {
                "id": 1,
                "first_name": "Martin",
                "last_name": "Alex",
                "date_of_birth": "1972-09-25",
                "gender": "m",
                "examine_date": "2024-03-30",
                "trimester": "1",
                "blood_group": "O+",
                "age": 52,
                "examine_by": "doctor",
                "email": "example@example.com",
                "phone_number": "123456789",
                "profile_image": null,
                "is_active": true
            },
            "response_message": "Patient details sent successfully."
        }
        """

        try:
            instance = self.get_object()

            return Response({
                    'response_code': status.HTTP_200_OK,
                    'data': self.get_serializer(instance).data,
                    'response_message': _('Patient details sent successfully.'),
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return handle_exceptions(e, 'Patient does not exist.')

    def delete(self, request, pk):
        """
        API to de-activate a Patient

        ### Example Request:
            DELETE /api/patients/<patient_id>/
        ### Example Response:
        {
            "response_code": 200,
            "data": {
                "id": 1,
                "first_name": "Martin",
                "last_name": "Alex",
                "date_of_birth": "1972-09-25",
                "gender": "m",
                "examine_date": "2024-03-30",
                "trimester": "1",
                "blood_group": "O+",
                "age": 52,
                "examine_by": "doctor",
                "email": "example@example.com",
                "phone_number": "123456789",
                "profile_image": null,
                "is_active": true
            },
            "response_message": "Patient details sent successfully."
        }
        """

        try:
            patient_to_deactivate = get_object_or_404(Patient, pk=pk)

            if patient_to_deactivate:
                patient_to_deactivate.is_active = False
                patient_to_deactivate.save()

            return Response({
                    "response_code": status.HTTP_200_OK,
                    "response_message": _('User De-activated successfully.'),
                    "data": self.get_serializer(patient_to_deactivate).data,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return handle_exceptions(e, 'User does not exist.')