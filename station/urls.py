from django.urls import path, include
from rest_framework import routers

from station.views import CrewViewSet, TrainTypeViewSet

router = routers.DefaultRouter()
router.register("crews", CrewViewSet, basename="crew")
router.register("train_types", TrainTypeViewSet, basename="train-type")

urlpatterns = [
    path("", include(router.urls))
]

app_name = "station"
