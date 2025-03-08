        
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Timetable
from api.serializers import TimetableSerializer

class CourseTimetableView(APIView):
    def get(self, request, course_id):
        try:
            timetables = Timetable.objects.filter(course_id=course_id)
            serializer = TimetableSerializer(timetables, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Timetable.DoesNotExist:
            return Response({"error": "Timetable not found"}, status=status.HTTP_404_NOT_FOUND)