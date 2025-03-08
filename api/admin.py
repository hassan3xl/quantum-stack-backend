from django.contrib import admin
from main.models import CustomUser, Project, Internship, Internship, Course, CourseMaterial, Timetable, InternshipApplication



admin.site.register(CustomUser)
admin.site.register(Project)

admin.site.register(Internship)
admin.site.register(InternshipApplication)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'description')

@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'material_type', 'course', 'uploaded_at')
    list_filter = ('material_type', 'course')
    search_fields = ('title', 'course__title')

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'start_time', 'end_time', 'is_live_session')
    list_filter = ('course', 'is_live_session')
    search_fields = ('title', 'course__title')