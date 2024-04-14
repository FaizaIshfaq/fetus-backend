from rest_framework import serializers

from .models import PatientExamine


class PatientExamineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientExamine
        fields = serializers.ALL_FIELDS
