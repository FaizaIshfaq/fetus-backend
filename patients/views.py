import datetime

from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, mixins, status, permissions
from rest_framework.response import Response
from rest_framework import generics, filters

from utils.mixins import PaginationMixin
from utils.paginations import FetusPageNumberPagination
from utils.exceptions import (
    handle_exceptions
)
from users.auth import UserTokenAuthentication
from doctors.models import Doctor
from .models import Patient
from .serializers import PatientSerializer


class PatientBaseAPIView(
    generics.ListAPIView,
    PaginationMixin,
):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = FetusPageNumberPagination
    authentication_classes = [UserTokenAuthentication]
    serializer_class = PatientSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email', 'phone_number']
    filterset_fields = {
        'examine_date': ["in"],
        'age': ["in"],
        'trimester': ["exact"],
        'examine_by': ["exact"],
    }

    def list(self, request, *args, **kwargs):
        """
        API to list all patients

        ### Example Request:
            GET /api/patients/
        ### Example Response:
        {
            "response_code": 200,
            "data": {
                "total_pages": 1,
                "count": 2,
                "next": null,
                "previous": null,
                "results": [
                    {
                        "id": 1,
                        "first_name": "khj",
                        "last_name": "njklhj",
                        "date_of_birth": "2024-04-12",
                        "examine_date": "2024-04-12",
                        "trimester": "1",
                        "blood_group": "O+",
                        "age": 22,
                        "email": null,
                        "phone_number": "98765432",
                        "profile_image": null,
                        "is_active": true,
                        "examine_by": {
                            "id": 1,
                            "name": "Doctor 1",
                            "gender": "m",
                            "qualification": "MBBS",
                            "specialization": "Spec-1"
                        }
                    },
                    {
                        "id": 2,
                        "first_name": "f",
                        "last_name": "i",
                        "date_of_birth": "2001-10-20",
                        "examine_date": "2024-06-06",
                        "trimester": "2",
                        "blood_group": "O+",
                        "age": 21,
                        "email": null,
                        "phone_number": "923022409",
                        "profile_image": null,
                        "is_active": true,
                        "examine_by": {
                            "id": 1,
                            "name": "Doctor 1",
                            "gender": "m",
                            "qualification": "MBBS",
                            "specialization": "Spec-1"
                        }
                    }
                ]
            },
            "response_message": "User details sent successfully."
        }
        """

        try:
            page = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
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
            return handle_exceptions(e, 'No patients details found.')


class PatientAppointmentsAPIView(
    PatientBaseAPIView
):
    queryset = Patient.objects.filter(
        is_active=True, examine_date__gte=datetime.date.today()
    ).order_by('id')


class PatientViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    PatientBaseAPIView,
):
    queryset = Patient.objects.filter(is_active=True).order_by('id')

    def create(self, request, *args, **kwargs):
        """
        API to create a new patient.

        ### Example Request:
            POST /api/patients/
            {
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": "2001-10-20",
                "examine_date": "2024-06-06",
                "trimester": "2",
                "blood_group": "O+",
                "age": 21,
                "examine_by": 1,
                "phone_number": "1234567890",
                "profile_image": <file_to_upload>
            }
        ### Example Response:
            {
                "response_code": 201,
                "response_message": "Patient created successfully.",
                "data": {
                    "patient": {
                        "id": 8,
                        "first_name": "John",
                        "last_name": "Doe",
                        "date_of_birth": "2001-10-20",
                        "examine_date": "2024-06-06",
                        "trimester": "2",
                        "blood_group": "O+",
                        "age": 21,
                        "examine_by": {
                            "id": 1,
                            "name": "Doctor 1",
                            "gender": "m",
                            "qualification": "MBBS",
                            "specialization": "Spec-1",
                        },
                        "email": null,
                        "phone_number": "1234567890",
                        "profile_image": null,
                        "is_active": true
                    }
                }
            }
        """

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            if Patient.objects.filter(phone_number=serializer.validated_data.get('phone_number')).exists():
                return Response({
                    "response_code": status.HTTP_400_BAD_REQUEST,
                    "response_message": "Patient with this phone number already exists.",
                    "data": None
                }, status=status.HTTP_400_BAD_REQUEST)

            patient = serializer.save()

            examine_by = request.data.get('examine_by')
            if examine_by:
                try:
                    doctor = Doctor.objects.get(id=examine_by)
                    patient.examine_by = doctor
                except Doctor.DoesNotExist:
                    return Response({
                        "response_code": status.HTTP_400_BAD_REQUEST,
                        "response_message": "Doctor with the provided ID does not exist.",
                        "data": None
                    }, status=status.HTTP_400_BAD_REQUEST)

            patient.is_active = True
            patient.save()

            return Response({
                "response_code": status.HTTP_201_CREATED,
                "response_message": "Patient created successfully.",
                "data": {
                    "patient": serializer.data
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            handle_exceptions(e, 'Unable to create patient')

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
                "examine_by": {
                     "id": 1,
                    "name": "Doctor 1",
                    "gender": "m",
                    "qualification": "MBBS",
                    "specialization": "Spec-1",
                },
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

    def update(self, request, *args, **kwargs):
        """
        API to update Patient fields

        ### Example Request:
            PUT /api/patients/<patient_id>/
            {
                "first_name": "f",
                "last_name": "i",
                "date_of_birth": "2001-10-20",
                "examine_date": "2024-6-06",
                "trimester": "2",
                "blood_group": "O+",
                "age": 21,
                "examine_by": 1,
                "phone_number": "92302240912",
                "profile_image": "image_to_upload"
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
                    "examine_by": {
                        "id": 1,
                        "name": "Doctor 1",
                        "gender": "m",
                        "qualification": "MBBS",
                        "specialization": "Spec-1",
                    },
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
                "examine_by": {
                    "id": 1,
                    "name": "Doctor 1",
                    "gender": "m",
                    "qualification": "MBBS",
                    "specialization": "Spec-1",
                },
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
                    "response_message": _('Patient De-activated successfully.'),
                    "data": self.get_serializer(patient_to_deactivate).data,
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return handle_exceptions(e, 'Patient does not exist.')
