from rest_framework import serializers
from main.models import Internship, CustomUser, Course, CourseMaterial, Timetable, InternshipApplication

from rest_framework import serializers
from main.models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'user', 'email', 'title', 'description', 'created_at', 'expected_completion_date', 'status', 'payment_status']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
class InternshipApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternshipApplication
        fields = ['email', 'mode']
        
class CourseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaterial
        fields = ['id', 'title', 'material_type', 'file', 'uploaded_at']

class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = ['id', 'title', 'start_time', 'end_time', 'is_live_session', 'location']

class CourseSerializer(serializers.ModelSerializer):
    materials = CourseMaterialSerializer(many=True, read_only=True)
    timetables = TimetableSerializer(many=True, read_only=True)  # Include timetables

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'category', 'language', 'framework', 'created_at', 'materials', 'timetables']

class InternshipSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Internship
        fields = '__all__'


