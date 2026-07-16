from django.db import models
from django.contrib.auth.models import User


# ==================================================
# STUDENT
# ==================================================
class Student(models.Model):

    # Login account connected to this student
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="student_profile"
    )

    name = models.CharField(
        max_length=100
    )

    roll_number = models.CharField(
        max_length=20,
        unique=True
    )

    email = models.EmailField()

    course = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name
class Faculty(models.Model):
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Course(models.Model):
    name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)

    def __str__(self):
        return self.name
class Attendance(models.Model):
    student_name = models.CharField(max_length=100)
    date = models.DateField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.student_name
class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.name} - {self.status}"   
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    marks = models.IntegerField()
    grade = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.student.name} - {self.subject}"                             
class Notice(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.title
class Timetable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.course.name} - {self.subject}"  
class Department(models.Model):
    name = models.CharField(max_length=100)
    department_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name                      
class Subject(models.Model):
    name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Assignment(models.Model):
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    description = models.TextField()
    due_date = models.DateField()

    def __str__(self):
        return self.title


class LeaveRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    reason = models.TextField()
    from_date = models.DateField()
    to_date = models.DateField()
    status = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return f"{self.student.name} - {self.status}"


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateField()

    def __str__(self):
        return self.title    
