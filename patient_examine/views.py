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
from model.femur.model import predict_femur_length
from model.head.model import predict_gestational_age

from .serializers import PatientExamineSerializer


def examine_patient(patient_examine):
    femur_length = predict_femur_length(
        patient_examine.femur_image,
        patient_examine.femur_pixel_depth
    )

    if femur_length is None:
        patient_examine.delete()
        raise PatientExamineException('Unable to examine patient femur.')

    gestational_age = predict_gestational_age(
        patient_examine.head_image,
        patient_examine.head_pixel_depth
    )

    if gestational_age is None:
        patient_examine.delete()
        raise PatientExamineException('Unable to examine patient gestational age.')

    patient_examine.femur_length = femur_length
    patient_examine.gestational_age = gestational_age
    patient_examine.save()

    return patient_examine


class PatientExamineAPIView(
    generics.CreateAPIView
):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [UserTokenAuthentication]
    serializer_class = PatientExamineSerializer

    def create(self, request, *args, **kwargs):
        """
        API to examine a patient.

        ### Example Request:
            POST /api/patient/examine/
            {
                "patient": 1,
                "femur_image": "path_to_image",
                "head_image": "path_to_image",
                "femur_pixel_depth": 0.114338452166,
                "head_pixel_depth": 0.0691358041432,
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

            patient_id = request.data.get('patient')
            if patient_id is None:
                return Response({
                    "response_code": status.HTTP_400_BAD_REQUEST,
                    "response_message": _("Patient with the provided ID does not exist."),
                    "data": None
                }, status=status.HTTP_400_BAD_REQUEST)

            patient = get_object_or_404(Patient, pk=patient_id)

            if patient.examine is None:
                examine = serializer.save()
            else:
                examine = patient.examine
                examine.femur_image = serializer.validated_data.get('femur_image')
                examine.head_image = serializer.validated_data.get('head_image')
                examine.femur_pixel_depth = serializer.validated_data.get('femur_pixel_depth')
                examine.head_pixel_depth = serializer.validated_data.get('head_pixel_depth')
                examine.save()

            # Examine patient data
            examine = examine_patient(examine)

            patient.examine = examine
            patient.save()

            return Response({
                "response_code": status.HTTP_201_CREATED,
                "response_message": _("Patient examined successfully."),
                "data": {
                    'id': examine.id,
                    'femur_image': f'/media/{examine.femur_image.name}',
                    'head_image': f'/media/{examine.head_image.name}',
                    'femur_pixel_depth': examine.femur_pixel_depth,
                    'head_pixel_depth': examine.head_pixel_depth,
                    'femur_number': examine.femur_number,
                    'femur_length': examine.femur_length,
                    'gestational_age': examine.gestational_age
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return handle_exceptions(e, 'Patient with the provided ID does not exist.')
