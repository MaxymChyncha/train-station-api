from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from station.models import Ticket
from station.serializers.trip_serializers import TripListSerializer


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = (
            "id",
            "cargo",
            "seat",
            "trip",
        )

    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs.get("cargo"),
            attrs.get("seat"),
            attrs.get("trip").train,
            ValidationError
        )
        return data


class TicketListSerializer(TicketSerializer):
    trip = TripListSerializer(many=False, read_only=True)
