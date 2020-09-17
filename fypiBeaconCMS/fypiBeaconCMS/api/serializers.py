from rest_framework import routers, serializers, viewsets
from catalog.models import Student, Classroom, Teacher





class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model=Teacher
        fields = '__all__'


class ClassroomSerializer(serializers.ModelSerializer):
    currentTeacher = TeacherSerializer()
    class Meta:
        model = Classroom
        fields = '__all__'
        excluded = ''
        

# Serializers define the API representation.
class StudentSerializer(serializers.ModelSerializer):
    attendanceClassroom = ClassroomSerializer()
    
    class Meta:
        model = Student
        fields = '__all__'
        
