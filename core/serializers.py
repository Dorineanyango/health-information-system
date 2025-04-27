from rest_framework import serializers
from .models import Client, Enrollment, HealthProgram

# Serializer for the HealthProgram model
class HealthProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthProgram
        fields = ['id', 'name', 'description']  

# Serializer for the Client model
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'age', 'gender', 'contact']  

# Serializer for the Enrollment model
class EnrollmentSerializer(serializers.ModelSerializer):
    program = HealthProgramSerializer()

    class Meta:
        model = Enrollment
        fields = ['id', 'program', 'enrolled_on'] 

# Serializer for the Client profile, including their enrollments
class ClientProfileSerializer(serializers.ModelSerializer):
    enrollments = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'name', 'age', 'gender', 'contact', 'enrollments']  

    # Method to retrieve and serialize the client's enrollments
    def get_enrollments(self, obj):
        enrollments = Enrollment.objects.filter(client=obj) 
        return EnrollmentSerializer(enrollments, many=True).data  