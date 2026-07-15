"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from dashboard.views import DashboardView
from rest_framework.routers import DefaultRouter
from django.urls import re_path
from dashboard.consumers import DashboardConsumer

router = DefaultRouter()
router.register(r'metrics', DashboardView, basename='metrics')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

websocket_urlpatterns = [
    re_path(r'ws/dashboard/$', DashboardConsumer.as_asgi()),
]
