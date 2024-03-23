from rest_framework import mixins, viewsets

from station.models import Crew, TrainType, Train
from station.serializers.crew_serializers import CrewSerializer
from station.serializers.train_serializers import TrainSerializer
from station.serializers.train_type_serializers import TrainTypeSerializer


class CrewViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class TrainTypeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer


class TrainViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
