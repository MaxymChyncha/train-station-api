from rest_framework import mixins, viewsets

from station.models import Crew
from station.serializers.crew_serializers import CrewSerializer


class CrewViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
