from datetime import datetime

from django.db.models import F, Count
from drf_spectacular.utils import extend_schema_view
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from station.models import Crew, TrainType, Train, Station, Route, Trip, Order
from station.paginations import OrderPagination
from station.serializers.crew_serializers import CrewSerializer
from station.serializers.order_serializers import (
    OrderSerializer,
    OrderListSerializer
)
from station.serializers.route_serializers import (
    RouteSerializer,
    RouteListSerializer,
    RouteDetailSerializer
)
from station.serializers.station_serializers import StationSerializer
from station.serializers.train_serializers import TrainSerializer
from station.serializers.train_type_serializers import TrainTypeSerializer
from station.serializers.trip_serializers import (
    TripSerializer,
    TripListSerializer,
    TripDetailSerializer
)
from station.utils.schemas import trip_list_schema, route_list_schema


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


class StationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


@extend_schema_view(
    list=route_list_schema()
)
class RouteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Route.objects.select_related("source", "destination")
    serializer_class = RouteSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            if source := self.request.query_params.get("source"):
                queryset = queryset.filter(source__name__icontains=source)

            if destination := self.request.query_params.get("destination"):
                queryset = queryset.filter(
                    destination__name__icontains=destination
                )

        return queryset.distinct()

    def get_serializer_class(self):

        if self.action == "list":
            return RouteListSerializer

        if self.action == "retrieve":
            return RouteDetailSerializer

        return self.serializer_class


@extend_schema_view(
    list=trip_list_schema()
)
class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == "list":
            current_time = datetime.now()
            queryset = (
                queryset
                .select_related(
                    "route__source",
                    "route__destination",
                    "train"
                )
                .filter(departure_time__gt=current_time)
                .annotate(
                    tickets_available=(
                        F("train__cargo_num")
                        * F("train__places_in_cargo")
                        - Count("tickets")
                    )
                )
            )

            if from_station := self.request.query_params.get("from"):
                queryset = queryset.filter(
                    route__source__name__icontains=from_station
                )

            if to_station := self.request.query_params.get("to"):
                queryset = queryset.filter(
                    route__destination__name__icontains=to_station
                )

            if departure := self.request.query_params.get("departure_date"):
                departure_date = datetime.strptime(departure, "%Y-%m-%d")
                queryset = queryset.filter(
                    departure_time__date=departure_date
                )

            if arrival := self.request.query_params.get("arrival_date"):
                arrival_date = datetime.strptime(arrival, "%Y-%m-%d")
                queryset = queryset.filter(
                    arrival_time__date=arrival_date
                )

        if self.action == "retrieve":
            queryset = (
                queryset
                .select_related(
                    "train__train_type",
                    "route__source",
                    "route__destination"
                )
                .prefetch_related("crew")
            )

        return queryset.distinct()

    def get_serializer_class(self):

        if self.action == "list":
            return TripListSerializer

        if self.action == "retrieve":
            return TripDetailSerializer

        return self.serializer_class


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Order.objects.prefetch_related(
        "tickets__trip__route__source",
        "tickets__trip__route__destination",
        "tickets__trip__train"
    )
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
