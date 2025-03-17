from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from main.models import CustomUser, Timetable, Internship, Project, Profile
from .serializers import InternshipSerializer, ProfileSerializer, ProjectSerializer, TimetableSerializer, InternshipApplicationSerializer
from django.contrib.auth import get_user_model 
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken



# from django.core.mail import send_mail

# def send_application_email(self, email):
#     subject = "Complete Your Internship Application"
#     message = f"Thank you for your interest! Please complete your application here: [Link to Form]"
#     from_email = "noreply@quantumstack.com"
#     recipient_list = [email]
#     send_mail(subject, message, from_email, recipient_list)

class SubmitProjectRequestView(APIView):
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            # Associate the project with the logged-in user if available
            if request.user.is_authenticated:
                serializer.save(user=request.user)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDetailView(APIView):
    def get(self, request, pk):
        try:
            project = Project.objects.get(id=pk)
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({"detail": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

class ProfileView(APIView):
    def get(self, request):
        user = request.user
        
        # Get or create profile for the user
        profile, created = Profile.objects.get_or_create(user=user)
        
        # Fetch internship and project data
        internships = Internship.objects.filter(intern=user)
        projects = Project.objects.filter(user=user)
        
        # Serialize profile data
        profile_data = ProfileSerializer(profile).data
        
        # Add related data to the response
        profile_data['internships'] = InternshipSerializer(internships, many=True).data
        profile_data['projects'] = ProjectSerializer(projects, many=True).data
        
        return Response(profile_data, status=status.HTTP_200_OK)
    
     
class ValidateInternshipView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not request.user.is_authenticated:
            raise NotAuthenticated("You are not authenticated.")

    def post(self, request):
        internship_id = request.data.get('internship_id')
        user = request.user

        # Check if the user has the provided internship_id and is an intern
        if user.internship_id == internship_id and user.is_intern:
            return Response({"message": "Access granted"}, status=status.HTTP_200_OK)
        return Response(
            {"error": "Invalid internship ID or you do not have permission"},
            status=status.HTTP_403_FORBIDDEN,
        )

class OngoingInternships(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        internships = Internship.objects.filter(intern=user)
        serializer = InternshipSerializer(internships, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CourseDetailsView(APIView):
    def get(self, request, pk):
        user = request.user
        try:
            internship = Internship.objects.get(id=pk, intern=user)
            if internship.status == 'Pending':
                return Response({"detail": "Your application is still pending. Please wait for approval."}, status=status.HTTP_403_FORBIDDEN)
            serializer = InternshipSerializer(internship)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Internship.DoesNotExist:
            return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)
    
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_authenticated:
            raise NotAuthenticated("You are not authenticated.")

        internships = Internship.objects.filter(intern=request.user)
        serializer = InternshipSerializer(internships, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseTimetableView(APIView):
    def get(self, request, course_id):
        try:
            timetables = Timetable.objects.filter(course_id=course_id)
            serializer = TimetableSerializer(timetables, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Timetable.DoesNotExist:
            return Response({"error": "Timetable not found"}, status=status.HTTP_404_NOT_FOUND)

class SubmitInitialApplicationView(APIView):
    def post(self, request):
        serializer = InternshipApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Send email with link to full application form
            # self.send_application_email(serializer.validated_data['email'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# Registration View
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # Validate input
        if not email or not password:
            return Response(
                {"error": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Create user
            user = CustomUser.objects.create_user(
                email=email,
                password=password
            )
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                "message": "User registered successfully",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # You can add custom claims here if needed
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Add user details to the response
        data['user'] = {
            'id': user.id,
            'email': user.email,
        }
        return data

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer