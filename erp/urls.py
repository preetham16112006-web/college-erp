from django.urls import path
from . import views


urlpatterns = [
    path(
    "student-services/",
    views.student_services,
    name="student_services"
),

    # =========================
    # DASHBOARD
    # =========================
    path("", views.home, name="home"),


    # =========================
    # STUDENT CRUD
    # =========================
    path("students/", views.student_list, name="student_list"),

    path(
        "students/add/",
        views.student_add,
        name="student_add"
    ),

    path(
        "students/<int:student_id>/edit/",
        views.student_edit,
        name="student_edit"
    ),

    path(
        "students/<int:student_id>/delete/",
        views.student_delete,
        name="student_delete"
    ),


    # =========================
    # ERP LIST PAGES
    # =========================
    path(
        "faculty/",
        views.faculty_list,
        name="faculty_list"
    ),

    path(
        "courses/",
        views.course_list,
        name="course_list"
    ),

    path(
        "subjects/",
        views.subject_list,
        name="subject_list"
    ),

    path(
    "student-attendance/",
    views.student_attendance,
    name="student_attendance"
    ),

    path(
        "attendance/",
        views.attendance_list,
        name="attendance_list"
    ),

    path(
        "notices/",
        views.notice_list,
        name="notice_list"
    ),

    path(
        "fees/",
        views.fee_list,
        name="fee_list"
    ),

    path(
        "results/",
        views.result_list,
        name="result_list"
    ),

    path(
        "timetables/",
        views.timetable_list,
        name="timetable_list"
    ),

    path(
        "assignments/",
        views.assignment_list,
        name="assignment_list"
    ),

    path(
        "events/",
        views.event_list,
        name="event_list"
    ),

    path(
        "leave-requests/",
        views.leave_request_list,
        name="leave_request_list"
    ),


    # =========================
    # STUDENT LOGIN SYSTEM
    # =========================
    path(
        "login/",
        views.student_login,
        name="student_login"
    ),

    path(
        "student-dashboard/",
        views.student_dashboard,
        name="student_dashboard"
    ),

    path(
        "logout/",
        views.student_logout,
        name="student_logout"
    ),

]