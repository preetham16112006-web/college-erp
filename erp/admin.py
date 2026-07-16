from django.contrib import admin
from .models import (
    Student,
    Faculty,
    Course,
    Attendance,
    Fee,
    Result,
    Notice,
    Timetable,
    Department,
    Subject,
    Assignment,
    LeaveRequest,
    Event,
)

admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(Attendance)
admin.site.register(Fee)
admin.site.register(Result)
admin.site.register(Notice)
admin.site.register(Timetable)
admin.site.register(Department)
admin.site.register(Subject)
admin.site.register(Assignment)
admin.site.register(LeaveRequest)
admin.site.register(Event)