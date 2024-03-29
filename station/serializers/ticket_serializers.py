from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from station.models import Ticket
from station.serializers.trip_serializers import TripOrderSerializer


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = (
            "id",
            "cargo",
            "seat",
            "trip",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Ticket.objects.all(),
                fields=("trip", "cargo", "seat",)
            )
        ]

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
    trip = TripOrderSerializer(many=False, read_only=True)
