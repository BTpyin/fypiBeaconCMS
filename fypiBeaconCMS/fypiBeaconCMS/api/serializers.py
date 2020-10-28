from rest_framework import routers, serializers, viewsets
from catalog.models import Student, Classroom, Teacher, Beacon,Course,Class


def set_required(options,isRequired):    
    fields = [field.name for field in options]
    return {f:{'required':isRequired} for f in fields}


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        requires_context=False
        model=Teacher
        fields = '__all__'


class ClassroomSerializer(serializers.ModelSerializer):
    currentTeacher = TeacherSerializer()
    class Meta:
        requires_context=False
        model = Classroom
        fields = '__all__'
        excluded = ''
        extra_kwargs={
            **set_required(model._meta.get_fields(),False),
        }

class BeaconSerializer(serializers.ModelSerializer):
    class Meta:
        model= Beacon
        fields = '__all__'
        
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class ClassSerializer(serializers.ModelSerializer):
    course = CourseSerializer(required=False)
    class Meta:
        model = Class
        fields = '__all__'
        
# Serializers define the API representation.
class StudentSerializer(serializers.ModelSerializer):
    attendanceClassroom = ClassroomSerializer(required=False)
    taking_class = ClassSerializer(required =False,many=True)
    
    class Meta:
        model = Student
        requires_context=False
        fields = '__all__'
        extra_kwargs = {
            **set_required(model._meta.get_fields(),False),
            'attendanceClassroom':{'required':False},   
            'taking_class' :{'required':False}                     
            }
            # 'url': {'view_name': 'student_detail', 'lookup_field': 'studentId'},
            # 'attendanceClassroom': {'lookup_field': 'classroomId'}
        
