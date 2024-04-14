from django.utils.translation import gettext_lazy as _

from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions, generics
from rest_framework.response import Response

from utils.exceptions import (
    handle_exceptions,
    PatientExamineException
)
from users.auth import UserTokenAuthentication
from patients.models import Patient
from model.femur_model import predict_femur_length_and_age
from model.head_model import predict_head_circumference_and_age

from .serializers import PatientFemurExamineSerializer, PatientHeadExamineSerializer


class PatientFemurExamineAPIView(
    generics.CreateAPIView
):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [UserTokenAuthentication]
    serializer_class = PatientFemurExamineSerializer

    def create(self, request, *args, **kwargs):
        """
        API to examine a patient.

        ### Example Request:
            POST /api/patient/<patient_id>/femur-examine/
            {
                "femur_image": "path_to_image",
                "pixel_depth": 0.114338452166,
            }
        ### Example Response:
            {
                "response_code": 201,
                "response_message": "Patient femur examined successfully.",
                "data": {
                    "id": 3,
                    "femur_image": "/media/WhatsApp_Image_2024-04-14_at_9.12.16_PM_jEPY1qe.jpeg",
                    "pixel_depth": 0.114338452166,
                    "femur_length": 42.78794816241332,
                    "femur_age": 23.334727500182524
                }
            }
        """

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            patient_id = kwargs['id']
            if patient_id is None:
                return Response({
                    "response_code": status.HTTP_400_BAD_REQUEST,
                    "response_message": _("Patient with the provided ID does not exist."),
                    "data": None
                }, status=status.HTTP_400_BAD_REQUEST)

            patient = get_object_or_404(Patient, pk=patient_id)
            if patient.femur_examine is None:
                examine = serializer.save()
            else:
                examine = patient.femur_examine
                examine.femur_image = serializer.validated_data.get('femur_image')
                examine.pixel_depth = serializer.validated_data.get('pixel_depth')
                examine.save()

            femur_length, femur_age = predict_femur_length_and_age(
                examine.femur_image,
                examine.pixel_depth
            )

            if femur_length is None or femur_age is None:
                examine.delete()
                raise PatientExamineException('Unable to examine patient femur.')

            examine.femur_length = femur_length
            examine.femur_age = femur_age
            examine.save()

            patient.femur_examine = examine
            patient.save()

            return Response({
                "response_code": status.HTTP_201_CREATED,
                "response_message": _("Patient femur examined successfully."),
                "data": {
                    'id': examine.id,
                    'femur_image': f'/media/{examine.femur_image.name}',
                    'pixel_depth': examine.pixel_depth,
                    'femur_length': examine.femur_length,
                    'femur_age': examine.femur_age
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return handle_exceptions(e, 'Patient with the provided ID does not exist.')


class PatientHeadExamineAPIView(
    generics.CreateAPIView
):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [UserTokenAuthentication]
    serializer_class = PatientHeadExamineSerializer

    def create(self, request, *args, **kwargs):
        """
        API to examine a patient.

        ### Example Request:
            POST /api/patient/<patient_id>/head-examine/
            {
                "head_image": "path_to_image",
                "pixel_depth": 0.114338452166,
            }
        ### Example Response:
            {
                "response_code": 201,
                "response_message": "Patient head examined successfully.",
                "data": {
                    "id": 2,
                    "head_image": "/media/WhatsApp_Image_2024-04-14_at_9.12.14_PM_J98eLey.jpeg",
                    "pixel_depth": 0.0691358041432,
                    "head_circumference": 78.47560562783542,
                    "gestational_age": 12.838361380022754
                }
            }
        """

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            patient_id = kwargs['id']
            if patient_id is None:
                return Response({
                    "response_code": status.HTTP_400_BAD_REQUEST,
                    "response_message": _("Patient with the provided ID does not exist."),
                    "data": None
                }, status=status.HTTP_400_BAD_REQUEST)

            patient = get_object_or_404(Patient, pk=patient_id)
            if patient.head_examine is None:
                examine = serializer.save()
            else:
                examine = patient.head_examine
                examine.head_image = serializer.validated_data.get('head_image')
                examine.pixel_depth = serializer.validated_data.get('pixel_depth')
                examine.save()

            head_circumference, gestational_age = predict_head_circumference_and_age(
                examine.head_image,
                examine.pixel_depth
            )

            if head_circumference is None or gestational_age is None:
                examine.delete()
                raise PatientExamineException('Unable to examine patient head.')

            examine.head_circumference = head_circumference
            examine.gestational_age = gestational_age
            examine.save()

            patient.head_examine = examine
            patient.save()

            return Response({
                "response_code": status.HTTP_201_CREATED,
                "response_message": _("Patient head examined successfully."),
                "data": {
                    'id': examine.id,
                    'head_image': f'/media/{examine.head_image.name}',
                    'pixel_depth': examine.pixel_depth,
                    'head_circumference': examine.head_circumference,
                    'gestational_age': examine.gestational_age
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return handle_exceptions(e, 'Patient with the provided ID does not exist.')
