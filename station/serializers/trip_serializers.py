from rest_framework import serializers

from station.models import Trip, Ticket
from station.serializers.crew_serializers import CrewDetailSerializer
from station.serializers.route_serializers import RouteDetailSerializer
from station.serializers.train_serializers import TrainDetailSerializer


class TripSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trip
        fields = (
            "id",
            "route",
            "train",
            "crew",
            "departure_time",
            "arrival_time",
        )

    def validate(self, attrs):
        if attrs.get("departure_time") >= attrs.get("arrival_time"):
            raise serializers.ValidationError(
                "Departure time can't be bigger than arrival time"
            )

        return attrs


class TripListSerializer(TripSerializer):
    route = serializers.StringRelatedField(read_only=True)
    train_name = serializers.CharField(source="train.name", read_only=True)
    train_capacity = serializers.IntegerField(
        source="train.capacity", read_only=True
    )
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Trip
        fields = (
            "id",
            "route",
            "departure_time",
            "arrival_time",
            "train_name",
            "train_capacity",
            "tickets_available"
        )


class TripTicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ("cargo", "seat")


class TripDetailSerializer(TripSerializer):
    route = RouteDetailSerializer(read_only=True)
    train = TrainDetailSerializer(read_only=True)
    crew = CrewDetailSerializer(many=True, read_only=True)
    taken_tickets = TripTicketSerializer(
        source="tickets",
        many=True,
        read_only=True
    )

    class Meta(TripSerializer.Meta):
        fields = TripSerializer.Meta.fields + ("taken_tickets",)


class TripOrderSerializer(serializers.ModelSerializer):
    route = serializers.StringRelatedField(read_only=True)
    train_name = serializers.CharField(source="train.name", read_only=True)

    class Meta:
        model = Trip
        fields = (
            "route",
            "departure_time",
            "arrival_time",
            "train_name"
        )
