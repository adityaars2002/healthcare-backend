from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Doctor, Patient, PatientDoctorMapping, User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ["id", "name", "email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id",
            "name",
            "age",
            "gender",
            "phone",
            "address",
            "medical_history",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["created_by", "created_at"]


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "id",
            "name",
            "specialization",
            "email",
            "phone",
            "experience_years",
            "created_at",
        ]
        read_only_fields = ["created_at"]


class MappingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.name", read_only=True)
    doctor_name = serializers.CharField(source="doctor.name", read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ["id", "patient", "patient_name", "doctor", "doctor_name", "created_at"]
        read_only_fields = ["created_at"]

    def validate_patient(self, patient):
        # A user may only assign doctors to patients they created.
        if patient.created_by != self.context["request"].user:
            raise serializers.ValidationError("Patient not found.")
        return patient

    def validate(self, attrs):
        if PatientDoctorMapping.objects.filter(
            patient=attrs["patient"], doctor=attrs["doctor"]
        ).exists():
            raise serializers.ValidationError("This doctor is already assigned to this patient.")
        return attrs
