from django.db import models
import uuid
# Create your models here.


class Student(models.Model):
    first_name = models.CharField(max_length=100,
                                  blank=False,
                                  help_text='First Name')
    last_name = models.CharField(max_length=100,
                                 blank=False,
                                 help_text='Last Name')
    studentId = models.CharField(max_length=8,
                                 blank=False,
                                 help_text='First Name')

    attendanceClassroom = models.ForeignKey(
        'Classroom', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['studentId']

    def __str__(self):
        """String for representing the Model object."""
        return (self.first_name + ' ' + self.last_name)


class Teacher(models.Model):
    first_name = models.CharField(max_length=100,
                                  blank=False,
                                  help_text='First Name')
    last_name = models.CharField(max_length=100,
                                 blank=False,
                                 help_text='Last Name')
    teacherId = models.CharField(max_length=8,
                                 blank=False,
                                 help_text='First Name')

    class Meta:
        ordering = ['teacherId']

    def __str__(self):
        """String for representing the Model object."""
        return (self.first_name + ' ' + self.last_name)


class StudentList(models.Model):
    classroom = models.ForeignKey(
        'Classroom', on_delete=models.SET_NULL, null=True)
    # studList = models.models.ManyToManyField("app.Model", verbose_name=_(""))
    # studList = (Student.objects.filter(attendanceClassroom='classroom'))
    studentList = models.ManyToManyField(
        Student, help_text='Select students for this classrrom')
    class Meta:
        ordering = ['classroom']

    def __str__(self):
        """String for representing the Model object."""
        return (self.classroom.classroomId + ' Student List')


class Beacon(models.Model):
    id = models.UUIDField(max_length=20,
                          primary_key=True,
                          default=uuid.uuid4,
                          help_text='Unique ID for the beacon')
    major = models.CharField(max_length=20, blank=False)
    minor = models.CharField(max_length=20, blank=False)
    classroomId = models.ForeignKey(
        'Classroom', on_delete=models.SET_NULL, null=True)
    remarks = models.TextField(
        max_length=1000, help_text='Enter remarks of the beacon')

    class Meta:
        ordering = ['classroomId']


class Classroom(models.Model):
    classroomId = models.CharField(max_length=20)
    currentTeacher = models.ForeignKey(
        'Teacher', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return (self.classroomId)
