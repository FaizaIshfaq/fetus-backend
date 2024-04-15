from rest_framework import serializers

from .models import Patient

from doctors.serializers import DoctorSerializer
from patient_examine.serializers import PatientFemurExamineSerializer, PatientHeadExamineSerializer


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = serializers.ALL_FIELDS

    def to_representation(self, instance):
        response = super().to_representation(instance)

        response['examine_by'] = None \
            if instance.examine_by is None \
            else DoctorSerializer(instance.examine_by).data

        response['femur_examine'] = None \
            if instance.femur_examine is None \
            else PatientFemurExamineSerializer(instance.femur_examine).data

        response['head_examine'] = None \
            if instance.head_examine is None \
            else PatientHeadExamineSerializer(instance.head_examine).data

        return response
