from rest_framework import serializers

from .models import PatientFemurExamine, PatientHeadExamine


class PatientFemurExamineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientFemurExamine
        fields = serializers.ALL_FIELDS


class PatientHeadExamineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientHeadExamine
        fields = serializers.ALL_FIELDS
