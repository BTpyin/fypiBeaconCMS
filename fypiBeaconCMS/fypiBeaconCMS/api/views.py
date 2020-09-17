from django.shortcuts import get_object_or_404, render
from catalog.models import Student, Classroom, Teacher
from rest_framework import serializers, viewsets,permissions, status
from .serializers import StudentSerializer,ClassroomSerializer
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework import generics
import json
from django.http.response import HttpResponse
from django.http import HttpResponseBadRequest

# ViewSets define the view behavior.
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    
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
        return Response(status.HTTP_400_BAD_REQUEST,status=status.HTTP_400_BAD_REQUEST)