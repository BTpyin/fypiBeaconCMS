from django.db import models
import uuid
from django.db.models.signals import pre_save, post_save,m2m_changed
# Create your models here.


class Student(models.Model):
    first_name = models.CharField(max_length=100,
                                  blank=False,
                                  help_text='First Name')
    last_name = models.CharField(max_length=100,
                                 blank=False,
                                 help_text='Last Name')
    
    display_name = models.CharField(max_length=127,
                                 blank=True,
                                 help_text='Display Name in App')
    
    studentId = models.CharField(max_length=8,
                                 blank=False,
                                 help_text='First Name')
    
    program = models.CharField(max_length=127,
                                 blank=False,
                                 help_text='Deparment')
    
    major = models.CharField(max_length=127,
                                 blank=False,
                                 help_text='Deparment')
    

    attendanceClassroom = models.ForeignKey(
        'Classroom', on_delete=models.DO_NOTHING, blank = True, null=True)

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
    
    display_name = models.CharField(max_length=127,
                                 blank=False,
                                 help_text='Display Name in App')
    
    teacherId = models.CharField(max_length=8,
                                 blank=False,
                                 help_text='First Name')
    
    department = models.CharField(max_length=127,
                                 blank=False,
                                 help_text='Deparment')
    
    

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
        if hasattr(self.classroom,'classroomId'): classroomId = self.classroom.classroomId
        else: classroomId = ""
        return (classroomId + ' Student List')


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
        'Teacher', on_delete=models.SET_NULL, blank = True, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return (self.classroomId)

class Course(models.Model):
    """
    use below command to get all ForeignKey relate model
    course_obj.class_set.all()
    """
    course_code = models.CharField(max_length=31,blank=False)
    credit = models.PositiveSmallIntegerField(default=3)
    name = models.CharField(max_length=31,blank=False)
    
    def __str__(self):
        return self.course_code +" "+ self.name
    
    def save(self):
        super(Course, self).save()

class Class(models.Model):
    name = models.CharField(max_length=31,blank=True)
    # courseCode = models.CharField(max_length=31,blank=False)
    course = models.ForeignKey('Course',on_delete=models.SET_NULL, null=True)
    code = models.PositiveIntegerField(blank=False,null=False)
    session = models.PositiveIntegerField(blank=False,null=False)
    class_type = models.CharField(
        max_length=7,
        choices=[("L","Lecture"),("T","Tutorial"),("Lab","Lab")],
        default="L",        
    )
    
    teacher = models.ForeignKey(
        'Teacher', on_delete=models.SET_NULL, null=True)
    updated= models.DateTimeField(auto_now=True)
    date = models.DateTimeField()
    create_at = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField()
    classroom = models.ForeignKey('Classroom',on_delete=models.SET_NULL,null=True,blank=True)
    classId = models.CharField(max_length=63,blank=False,editable=False)
    
    def __str__(self):
        print(self.classId)
        return f'{self.course} {self.class_type}{self.code:02d} {self.session:02d}'
    
    def save(self):
        self.classId = f'{self.course.course_code}{self.class_type}{self.code:02d}{self.session:02d}'
        super(Class,self).save()