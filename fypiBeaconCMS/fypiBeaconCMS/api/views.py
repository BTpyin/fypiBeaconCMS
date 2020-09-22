from django.shortcuts import get_object_or_404, render
from catalog.models import Student, Classroom, Teacher, Beacon, StudentList, Class,Course
from rest_framework import serializers, viewsets,permissions, status
from .serializers import StudentSerializer,ClassroomSerializer, BeaconSerializer,CourseSerializer, ClassSerializer
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework import generics
from django.urls import reverse
import json
from django.http.response import HttpResponse
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect

# ViewSets define the view behavior.
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'studentId'
    
    
class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    
class BeaconViewSet(viewsets.ModelViewSet):
    queryset = Beacon.objects.all()
    serializer_class = BeaconSerializer
    
    
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def CheckSidValid(request):
    res = {
            "valid" : False
    }    
    try:
        qs = Student.objects.filter(studentId=request.GET['sid'])
        if qs is None or qs.count() <= 0:                        
            return Response(res)
        res['valid'] = True
        return Response(res)
    except:
        res = {'message':"Bad request"}
        return Response(res,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def GetStudentInfo(request, sid):
    return redirect(reverse('api:students-detail',args=[sid]))

@api_view(['POST','PUT'])
@permission_classes((permissions.AllowAny,))
def UpdateDisplayName(request,sid):
    """
    Exmaple
    data = 
    {
    "display_name": "Stanley"
    }
    """
    try:
        student = Student.objects.get(studentId=sid)
    except student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT' or request.method == 'POST':
        serializer = StudentSerializer(student,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def GetBeaconRepresent(request,id):
    try:
        beacon = Beacon.objects.get(id=id)
    except beacon.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    classroom = beacon.classroomId
    serializer = ClassroomSerializer(classroom)
    return Response({"classroomId":classroom.classroomId},status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def GetClassroomInfo(request,classroomId):
    try:
        classroom = Classroom.objects.get(classroomId=classroomId)
    except classroom.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    
    serializer = ClassroomSerializer(classroom)
    return Response(serializer.data,status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def TakeAttendance(request,classroomId):    
    try:
        student = Student.objects.get(studentId=request.data['sid'])
    except student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        classroom=Classroom.objects.get(classroomId=classroomId)
    except classroom.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    
    students,created = StudentList.objects.get_or_create(classroom=classroom)
    students.studentList.add(student)
    return Response({'message':'success'},status=status.HTTP_202_ACCEPTED)
    
@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def UpdateClassroomTeacher(request):
    classroomId = request.data["classroomId"]
    classId = request.data['classId']
    classroom = Classroom.objects.get(classroomId=classroomId)
    _class= Class.objects.get(classId=classId)
    classroom.currentTeacher = _class.teacher
    classroom.save()
    return Response({'message':"updated"},status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def RefreshAttendanceList(request):
    classroomId = request.data['classroomId']
    classroom = Classroom.objects.get(classroomId=classroomId)
    classroom.currentTeacher=None
    classroom.save()
    return Response({'message':"cleared"},status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def GetCourseDetail(request,courseId):
    try:
        course = Course.objects.get(course_code=courseId)
    except course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    classes = course.class_set.all()
    classes_json_list = [ClassSerializer(c).data for c in classes]
    serializer = CourseSerializer(course)
    data = serializer.data
    pop_course = [c.pop('course') for c in classes_json_list]
    data.update({'class':classes_json_list})
    print(dir(data))
    details = serializer.data.update({'class':classes_json_list})
    return Response(data,status=status.HTTP_202_ACCEPTED)

result = {
    "message" : "Bad request"
} 

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def GetClassInfo(request):
    try:
        _class = Class.objects.get(classId=request.GET['classId'])
        serializer = ClassSerializer(_class) 
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(result,status=status.HTTP_400_BAD_REQUEST)