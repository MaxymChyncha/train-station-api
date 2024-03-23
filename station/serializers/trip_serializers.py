from rest_framework import serializers

from station.models import Trip


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
