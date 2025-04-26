from rest_framework import serializers
from .models import Client, Enrollment, HealthProgram

class HealthProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthProgram
        fields = ['id', 'name', 'description']

class EnrollmentSerializer(serializers.ModelSerializer):
    program = HealthProgramSerializer()

    class Meta:
        model = Enrollment
        fields = ['id', 'program', 'enrolled_on']

class ClientProfileSerializer(serializers.ModelSerializer):
    enrollments = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'name', 'age', 'gender', 'contact', 'enrollments']

    def get_enrollments(self, obj):
        enrollments = Enrollment.objects.filter(client=obj)
        return EnrollmentSerializer(enrollments, many=True).data
