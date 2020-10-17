from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from rest_framework import routers, serializers, viewsets
from . import views



student_detail = views.StudentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'students', views.StudentViewSet,basename='students')
router.register(r'classroom', views.ClassroomViewSet)
router.register(r'beacon', views.BeaconViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^checkSidValid/',views.CheckSidValid, name='checkSidVaild'),
    path('getStudentInfo/<int:sid>/', views.GetStudentInfo, name='getStudentInfo'),
    path('updateDisplayName/<int:sid>',views.UpdateDisplayName,name="updateDisplayName"),
    path('getBeaconRepresent/',views.GetBeaconRepresent,name="getBeaconRepresent"),
    path('getClassroomInfo/<str:classroomId>',views.GetClassroomInfo,name="getClasseoomInfo"),
    path('takeAttendance/<str:classroomId>',views.TakeAttendance,name="takeAttendance"),
    path('updateClassroomTeacher/',views.UpdateClassroomTeacher),
    path('refreshAttendanceList/',views.RefreshAttendanceList),
    path('getCourseDetail/<str:courseId>',views.GetCourseDetail),
    path('getClassInfo/',views.GetClassInfo)
    # path('studentsView/', views.StudentViewSet.as_view()),
    # path('students/<int:pk>/', views.StudentViewSet.as_view()),
    # path('classroom/',views.ClassroomViewSet.as_view()),
]

