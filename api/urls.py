from django.urls import path
from .views import RegisterView, LoginView, ProfileView, CourseTimetableView, SubmitProjectRequestView, ProjectDetailView, SubmitInitialApplicationView, CourseDetailsView, DashboardView,OngoingInternships, ValidateInternshipView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", LoginView.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    
    
    path('validate-internship/', ValidateInternshipView.as_view(), name='validate-internship'),
    path("internships/", OngoingInternships.as_view(), name="ongoing-internships"),
    path("internships/new/", OngoingInternships.as_view(), name="ongoing-internships"),
    path("internships/<int:pk>/", CourseDetailsView.as_view(), name="course-details"),
    path('courses/<int:course_id>/timetable/', CourseTimetableView.as_view(), name='course-timetable'),
    path('submit-initial-application/', SubmitInitialApplicationView.as_view(), name='submit-initial-application'),
    path('submit-project-request/', SubmitProjectRequestView.as_view(), name='submit-project-request'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
    
    # ADMIN VIEW HERE
    path("timetable/", CourseTimetableView.as_view(), name="timetable"),
        
    

]