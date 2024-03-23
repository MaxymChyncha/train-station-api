from django.urls import path, include
from rest_framework import routers

from station.views import CrewViewSet

router = routers.DefaultRouter()
router.register("crews", CrewViewSet, basename="crew")

urlpatterns = [
    path("", include(router.urls))
]

app_name = "station"
