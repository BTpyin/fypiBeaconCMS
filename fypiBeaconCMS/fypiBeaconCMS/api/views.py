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
import requests

result = {
    "Success" : False,
    "Remarks" : "",
    "Value" : None
}

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
    res = result    
    try:
        qs = Student.objects.filter(studentId=request.GET['sid'])
        if qs is None or qs.count() <= 0:                      
            data = {"Valid":True}
            res.update({"Success":True,"Value":data})
            return Response(res)
        data = {"Valid":False}
        res.update({"Success":True,"Value":data,"Remarks":"Already Used"})
        return Response(res,status=status.HTTP_302_FOUND)
    except:
        return Response(res,status=status.HTTP_400_BAD_REQUEST)
    
    
def get_student_detail(sid):
    return redirect(reverse('api:students-detail',args=[sid]))

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def GetStudentInfo(request, sid):
    # return redirect(reverse('api:students-detail',args=[sid]))
    res = result
    link = request.get_raw_uri()
    api = link[:str(link).find("api/")]
    re = requests.get(api+"api/students/"+str(sid))    
    data = re.json()
    res.update({"Success":True,"Value":data})    
    return Response(res)

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
    res = result
    try:
        student = Student.objects.get(studentId=sid)
    except student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT' or request.method == 'POST':
        serializer = StudentSerializer(student,data=request.data)
        if serializer.is_valid():
            serializer.save()
            res.update({"Success":True,"Value":serializer.data})
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(res.update({"Success":False,"Remark":serializer.errors,"Value":None}), status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def GetBeaconRepresent(request,id):
    res =result
    try:
        beacon = Beacon.objects.get(id=id)
    except beacon.DoesNotExist:
        return Response(res,status=status.HTTP_404_NOT_FOUND)
    classroom = beacon.classroomId
    serializer = ClassroomSerializer(classroom)
    res.update({"Value":{"classroomId":classroom.classroomId}})
    return Response(res,status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def GetClassroomInfo(request,classroomId):
    res = result
    try:
        classroom = Classroom.objects.get(classroomId=classroomId)
    except classroom.DoesNotExist:
        return Response(res,status=status.HTTP_404_NOT_FOUND)    
    serializer = ClassroomSerializer(classroom)
    res.update({"Success":True,"Value":serializer.data})
    return Response(res,status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def TakeAttendance(request,classroomId):    
    res = result
    try:
        student = Student.objects.get(studentId=request.data['sid'])
    except KeyError as e:
        res.update({"Remarks":"please check the post data"})
        return Response(res,status=status.HTTP_400_BAD_REQUEST)
    except Student.DoesNotExist:
        res.update({"Remarks":"Studnet does not exist"})
        return Response(res,status=status.HTTP_404_NOT_FOUND)
    try:
        classroom=Classroom.objects.get(classroomId=classroomId)
    except Classroom.DoesNotExist:
        res.update({"Remarks":"Classroom does not exist"})
        return Response(res,status=status.HTTP_404_NOT_FOUND)    
    students,created = StudentList.objects.get_or_create(classroom=classroom)
    students.studentList.add(student)
    res.update({"Success":True,"Value":{'message':'success'}})
    return Response(res,status=status.HTTP_202_ACCEPTED)
    
@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def UpdateClassroomTeacher(request):
    res = result
    classroomId = request.data["classroomId"]
    classId = request.data['classId']
    classroom = Classroom.objects.get(classroomId=classroomId)
    _class= Class.objects.get(classId=classId)
    classroom.currentTeacher = _class.teacher
    classroom.save()
    res.update({"Success":True,"Value":{'message':"updated"}})
    return Response(res,status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def RefreshAttendanceList(request):
    res = result
    classroomId = request.data['classroomId']
    classroom = Classroom.objects.get(classroomId=classroomId)
    classroom.currentTeacher=None
    classroom.save()
    res.update({"Success":True,"Value":{'message':"cleared"}})
    return Response(res,status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def GetCourseDetail(request,courseId):
    res = result
    try:
        course = Course.objects.get(course_code=courseId)
    except course.DoesNotExist:
        res.update({"Remarks":"Course does not exist"})
        return Response(res,status=status.HTTP_404_NOT_FOUND)
    classes = course.class_set.all()
    classes_json_list = [ClassSerializer(c).data for c in classes]
    serializer = CourseSerializer(course)
    data = serializer.data
    pop_course = [c.pop('course') for c in classes_json_list]
    data.update({'class':classes_json_list})
    details = serializer.data.update({'class':classes_json_list})
    res.update({"Success":True,"Value":data})
    return Response(res,status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def GetClassInfo(request):
    res = result
    try:
        _class = Class.objects.get(classId=request.GET['classId'])
        serializer = ClassSerializer(_class) 
        res.update({"Success":True,"Value":serializer.data})
        return Response(res, status=status.HTTP_200_OK)
    except:
        return Response(res,status=status.HTTP_400_BAD_REQUEST)