from rest_framework import serializers

from .models import Patient

from doctors.serializers import DoctorSerializer


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = serializers.ALL_FIELDS

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['examine_by'] = DoctorSerializer(instance.examine_by).data
        return response
