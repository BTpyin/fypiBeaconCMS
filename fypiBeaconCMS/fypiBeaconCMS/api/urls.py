from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from rest_framework import routers, serializers, viewsets
from . import views







# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'students', views.StudentViewSet)
router.register(r'classroom', views.ClassroomViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^checkSidValid/',views.CheckSidValid, name='checkSidVaild')
    # path('studentsView/', views.StudentViewSet.as_view()),
    # path('students/<int:pk>/', views.StudentViewSet.as_view()),
    # path('classroom/',views.ClassroomViewSet.as_view()),
]

