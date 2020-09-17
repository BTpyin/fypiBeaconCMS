from django.urls import path,include
from . import views
from django.conf.urls import url,re_path
from django.views.generic import RedirectView


urlpatterns = [
    path('api/', include(('api.urls','api'),namespace='api')),
    re_path('',include(('api.urls','api')))
]