from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelform_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .models import (
    Student,
    Faculty,
    Course,
    Subject,
    Department,
    Attendance,
    Notice,
    Fee,
    Result,
    Timetable,
    Assignment,
    Event,
    LeaveRequest,
)


# ==================================================
# HOME / ERP DASHBOARD
# ==================================================

def home(request):
    context = {
        "student_count": Student.objects.count(),
        "faculty_count": Faculty.objects.count(),
        "course_count": Course.objects.count(),
        "subject_count": Subject.objects.count(),
        "department_count": Department.objects.count(),
        "attendance_count": Attendance.objects.count(),
        "notice_count": Notice.objects.count(),
    }

    return render(request, "home.html", context)


# ==================================================
# STUDENT FORM
# ==================================================

StudentForm = modelform_factory(
    Student,
    fields=[
        "name",
        "roll_number",
        "email",
        "course",
        "profile_photo",
        "address",
        "phone_number_1",
        "phone_number_2",
        "caste",
        "religion",
        "nationality",
        "admission_number",
        "stats_number",
    ]
)


# ==================================================
# STUDENT LIST
# ==================================================

def student_list(request):
    students = Student.objects.all().order_by("id")

    return render(
        request,
        "student_list.html",
        {
            "items":students,
            "tittle":students,
        }
    )


# ==================================================
# ADD STUDENT
# ==================================================

def student_add(request):

    if request.method == "POST":
        form = StudentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()
            return redirect("student_list")

    else:
        form = StudentForm()

    return render(
        request,
        "student_add.html",
        {
            "form": form,
            "title": "Add Student",
        }
    )


# ==================================================
# EDIT STUDENT
# ==================================================

def student_edit(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id
    )

    if request.method == "POST":
        form = StudentForm(
            request.POST,
            request.FILES,
            instance=student
        )

        if form.is_valid():
            form.save()
            return redirect("student_list")

    else:
        form = StudentForm(
            instance=student
        )

    return render(
        request,
        "student_add.html",
        {
            "form": form,
            "title": "Edit Student",
            "student": student,
        }
    )


# ==================================================
# DELETE STUDENT
# ==================================================

def student_delete(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id
    )

    if request.method == "POST":   
        student.delete()
        return redirect("student_list")

    return render(
        request,
        "student_delete.html",
        {
            "student": student
        }
    )


# ==================================================
# GENERIC LIST PAGE
# ==================================================

def show_list(request, model, title):

    objects = model.objects.all().order_by("id")

    return render(
        request,
        "list.html",
        {
            "objects": objects,
            "title": title,
        }
    )


# ==================================================
# FACULTY
# ==================================================

def faculty_list(request):
    return show_list(
        request,
        Faculty,
        "Faculty"
    )


# ==================================================
# COURSES
# ==================================================

def course_list(request):
    return show_list(
        request,
        Course,
        "Courses"
    )


# ==================================================
# SUBJECTS
# ==================================================

def subject_list(request):
    return show_list(
        request,
        Subject,
        "Subjects"
    )


# ==================================================
# DEPARTMENTS
# ==================================================

def department_list(request):
    return show_list(
        request,
        Department,
        "Departments"
    )


# ==================================================
# ATTENDANCE
# ==================================================

def attendance_list(request):
    return show_list(
        request,
        Attendance,
        "Attendance"
    )


# ==================================================
# NOTICES
# ==================================================

def notice_list(request):
    return show_list(
        request,
        Notice,
        "Notices"
    )


# ==================================================
# FEES
# ==================================================

def fee_list(request):
    return show_list(
        request,
        Fee,
        "Fees"
    )


# ==================================================
# RESULTS
# ==================================================

def result_list(request):
    return show_list(
        request,
        Result,
        "Results"
    )


# ==================================================
# TIMETABLES
# ==================================================

def timetable_list(request):
    return show_list(
        request,
        Timetable,
        "Timetables"
    )


# ==================================================
# ASSIGNMENTS
# ==================================================

def assignment_list(request):
    return show_list(
        request,
        Assignment,
        "Assignments"
    )


# ==================================================
# EVENTS
# ==================================================

def event_list(request):
    return show_list(
        request,
        Event,
        "Events"
    )


# ==================================================
# LEAVE REQUESTS
# ==================================================

def leave_request_list(request):
    return show_list(
        request,
        LeaveRequest,
        "Leave Requests"
    )


# ==================================================
# STUDENT LOGIN
# ==================================================

def student_login(request):

    # If a student is already logged in,
    # send them directly to their dashboard.
    if request.user.is_authenticated:

        if hasattr(
            request.user,
            "student_profile"
        ):
            return redirect(
                "student_dashboard"
            )

    error = None

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # Only a User connected to a Student
            # can use the student dashboard.
            if hasattr(
                user,
                "student_profile"
            ):

                login(
                    request,
                    user
                )

                return redirect(
                    "student_dashboard"
                )

            else:
                error = (
                    "This account is not connected "
                    "to a student."
                )

        else:
            error = (
                "Invalid username or password."
            )

    return render(
        request,
        "student_login.html",
        {
            "error": error
        }
    )


# ==================================================
# STUDENT DASHBOARD
# ==================================================

@login_required(
    login_url="student_login"
)
def student_dashboard(request):

    # User must have a Student profile.
    if not hasattr(
        request.user,
        "student_profile"
    ):
        logout(request)

        return redirect(
            "student_login"
        )

    student = (
        request.user.student_profile
    )

    context = {
        "student": student,
    }

    return render(
        request,
        "student_dashboard.html",
        context
    )


# ==================================================
# STUDENT LOGOUT
# ==================================================

def student_logout(request):

    logout(request)

    return redirect(
        "student_login"
    )
@login_required(login_url="student_login")
def student_attendance(request):
    if not hasattr(request.user, "student_profile"):
        logout(request)
        return redirect("student_login")

    student = request.user.student_profile

    attendance_qs = Attendance.objects.filter(
        student_name__iexact=student.name
    ).order_by("-date")

    now = datetime.now()
    month = request.GET.get("month", now.month)
    year = request.GET.get("year", now.year)

    try:
        month = int(month)
    except (TypeError, ValueError):
        month = now.month

    try:
        year = int(year)
    except (TypeError, ValueError):
        year = now.year

    if month < 1 or month > 12:
        month = now.month

    attendance_records = attendance_qs.filter(
        date__month=month,
        date__year=year
    )

    total_classes = attendance_records.count()
    attended_classes = attendance_records.filter(
        status__iexact="present"
    ).count()
    absent_classes = attendance_records.filter(
        status__iexact="absent"
    ).count()

    attendance_percentage = 0
    if total_classes > 0:
        attendance_percentage = round(
            (attended_classes / total_classes) * 100,
            2
        )

    if attendance_percentage >= 80:
        attendance_band = "Excellent"
    elif attendance_percentage >= 60:
        attendance_band = "Average"
    else:
        attendance_band = "Needs Improvement"

    available_years = attendance_qs.dates(
        "date",
        "year",
        order="DESC"
    )
    year_options = [item.year for item in available_years]
    if year not in year_options:
        year_options.append(year)
        year_options.sort(reverse=True)

    context = {
        "student": student,
        "attendance_records": attendance_records,
        "selected_month": month,
        "selected_year": year,
        "total_classes": total_classes,
        "attended_classes": attended_classes,
        "absent_classes": absent_classes,
        "attendance_percentage": attendance_percentage,
        "attendance_band": attendance_band,
        "month_options": [
            (1, "January"), (2, "February"), (3, "March"),
            (4, "April"), (5, "May"), (6, "June"),
            (7, "July"), (8, "August"), (9, "September"),
            (10, "October"), (11, "November"), (12, "December"),
        ],
        "year_options": year_options,
    }

    return render(
        request,
        "student_attendance.html",
        context
    )
@login_required(login_url="student_login")
def student_services(request):

    # Check whether the logged-in user has a student profile
    if not hasattr(request.user, "student_profile"):
        logout(request)
        return redirect("student_login")

    # Get logged-in student's profile
    student = request.user.student_profile

    # Get this student's fee records
    fees = Fee.objects.filter(student=student)

    # Get this student's result records
    results = Result.objects.filter(student=student)

    # Get timetable records
    timetable = Timetable.objects.filter(
        course__name__iexact=student.course.strip()
    )

    # Get assignment records
    assignments = Assignment.objects.all()

    # Get notices, newest first
    notices = Notice.objects.all().order_by("-date")

    # Send data to student_services.html
    context = {
        "student": student,
        "fees": fees,
        "results": results,
        "timetable": timetable,
        "assignments": assignments,
        "notices": notices,
    }

    return render(
        request,
        "student_services.html",
        context
    )


@login_required(login_url="student_login")
def student_fees(request):
    if not hasattr(request.user, "student_profile"):
        logout(request)
        return redirect("student_login")

    student = request.user.student_profile
    fees = Fee.objects.filter(student=student)

    return render(
        request,
        "student_fees.html",
        {
            "student": student,
            "fees": fees,
        }
    )


@login_required(login_url="student_login")
def student_results(request):
    if not hasattr(request.user, "student_profile"):
        logout(request)
        return redirect("student_login")

    student = request.user.student_profile
    results = Result.objects.filter(student=student)

    return render(
        request,
        "student_results.html",
        {
            "student": student,
            "results": results,
        }
    )


@login_required(login_url="student_login")
def student_timetable(request):
    if not hasattr(request.user, "student_profile"):
        logout(request)
        return redirect("student_login")

    student = request.user.student_profile

    timetable = Timetable.objects.filter(
        course__name__iexact=student.course.strip()
    )

    return render(
        request,
        "student_timetable.html",
        {
            "student": student,
            "timetable": timetable,
        }
    )


@login_required(login_url="student_login")
def student_notices(request):
    if not hasattr(request.user, "student_profile"):
        logout(request)
        return redirect("student_login")

    student = request.user.student_profile
    notices = Notice.objects.all().order_by("-date")

    return render(
        request,
        "student_notices.html",
        {
            "student": student,
            "notices": notices,
        }
    )


@login_required(login_url="student_login")
def student_assignments(request):
    if not hasattr(request.user, "student_profile"):
        logout(request)
        return redirect("student_login")

    student = request.user.student_profile
    assignments = Assignment.objects.all()

    return render(
        request,
        "student_assignments.html",
        {
            "student": student,
            "assignments": assignments,
        }
    )