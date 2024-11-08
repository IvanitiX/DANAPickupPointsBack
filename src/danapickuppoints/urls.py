"""
URL configuration for danapickuppoints project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework import routers
from town.views import TownListView
from timetable.views import TimetableView
from pickup_point.views import PickupPointView
from report.views import ReportView

router = routers.DefaultRouter()
router.register(
    r"town",
    TownListView,
    basename='towns'
)
router.register(
    r"timetable",
    TimetableView,
    basename='timetable'
)
router.register(
    r"pickup_point",
    PickupPointView,
    basename='pickup_point'
)
router.register(
    r"report",
    ReportView,
    basename='report'
)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/v1/', include((router.urls,'v1'), namespace='v1')),
]