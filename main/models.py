from django.db import models 
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.core.validators import EmailValidator


# models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not email:
            raise ValueError('The Email field must be set')
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    internship_id = models.CharField(max_length=12, blank=True, null=True)
    is_intern = models.BooleanField(default=False)   
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    


class ContactUs(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    message = models.CharField(max_length=150)
    

class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    

class Project(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)  # Optional if user is logged in
    email = models.EmailField(validators=[EmailValidator()], null=False, blank=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expected_completion_date = models.DateField(null=True, blank=True)  # Set by admin
    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Processing", "Processing"),
            ("Completed", "Completed"),
            ("Cancelled", "Cancelled"),
        ],
        default="Pending",
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Paid", "Paid"),
            ("Failed", "Failed"),
        ],
        default="Pending",
    )

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

class Course(models.Model):
    COURSE_CHOICES = [
        ('software_dev', 'Software Development'),
        ('data_science', 'Data Science'),
        ('Cloud Engeneering', 'Cloud Engeneering'),
        ('DevOps Engeneering', 'DevOps Engeneering'),
        
    ]

    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('java', 'Java'),
        ('ruby', 'Ruby'),
        ('csharp', 'C#'),
    ]

    FRAMEWORK_CHOICES = [
        ('django', 'Django'),
        ('react', 'React'),
        ('flask', 'Flask'),
        ('vue', 'Vue.js'),
        ('angular', 'Angular'),
    ]

    title = models.CharField(max_length=255, help_text="Title of the course")
    description = models.TextField(help_text="Description of the course", null=True, blank=True)
    category = models.CharField(max_length=50, choices=COURSE_CHOICES, help_text="Category of the course")
    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES, help_text="Language used in the course")
    framework = models.CharField(max_length=50, choices=FRAMEWORK_CHOICES, help_text="Framework used in the course")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.language} - {self.framework})"
    
    
class InternshipApplication(models.Model):
    MODE_CHOICES = [
        ('siwes', 'SIWES'),
        ('bootcamp', 'Training Bootcamp'),
        ('remote', 'Remote Internship'),
    ]

    email = models.EmailField(validators=[EmailValidator()])
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.get_mode_display()}"
    
class Internship(models.Model):
    intern = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='internships')
    created_at = models.DateTimeField(auto_now_add=True)
    starting_date = models.DateField()
    completion_date = models.DateField()
    duration = models.CharField(
        max_length=20,
        choices=[
            ("3 Months", "3 Months"),
            ("6 Months", "6 Months"),
            ("9 Months", "9 Months"),
            ("12 Months", "12 Months"),
        ],
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Ongoing", "Ongoing"),
            ("Completed", "Completed"),
            ("Cancelled", "Cancelled"),
        ],
        default="Pending",
    )

    def clean(self):
        # Ensure completion_date is after starting_date
        if self.completion_date <= self.starting_date:
            raise ValidationError("Completion date must be after the starting date.")

    def __str__(self):
        return f"{self.intern.email} Internship ({self.course.title})"


class CourseMaterial(models.Model):
    MATERIAL_TYPE_CHOICES = [
        ('video', 'Video'),
        ('image', 'Image'),
        ('pdf', 'PDF'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')  # Link to Course
    title = models.CharField(max_length=255, help_text="Title of the material")
    material_type = models.CharField(max_length=10, choices=MATERIAL_TYPE_CHOICES, help_text="Type of the material")
    file = models.FileField(
        upload_to='course_materials/',
        validators=[
            FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi', 'jpg', 'jpeg', 'png', 'pdf'])
        ],
        help_text="Upload a video, image, or PDF file"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_material_type_display()})"

class Timetable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='timetables')
    title = models.CharField(max_length=255, help_text="Title of the timetable entry (e.g., 'Week 1: Introduction')")
    start_time = models.DateTimeField(help_text="Start time of the session or task")
    end_time = models.DateTimeField(help_text="End time of the session or task")
    is_live_session = models.BooleanField(default=False, help_text="Is this a live session?")
    location = models.CharField(max_length=255, blank=True, null=True, help_text="Location of the session (if applicable)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.title})"