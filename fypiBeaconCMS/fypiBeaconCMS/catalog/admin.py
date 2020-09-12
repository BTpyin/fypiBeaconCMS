from django.contrib import admin

# Register your models here.

from .models import Beacon, Classroom, Student, Teacher, StudentList

admin.site.register(Beacon)
admin.site.register(Classroom)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(StudentList)
