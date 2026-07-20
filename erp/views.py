from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelform_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
        form = StudentForm(request.POST)

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

    attendance_records = Attendance.objects.filter(
        student_name__iexact=student.name
    ).order_by("-date")

    context = {
        "student": student,
        "attendance_records": attendance_records,
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
       