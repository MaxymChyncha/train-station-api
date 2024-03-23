from rest_framework import serializers

from station.models import Route


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = (
            "id",
            "source",
            "destination",
            "distance",
        )

    def validate(self, attrs):
        if attrs.get("source") == attrs.get("destination"):
            raise serializers.ValidationError(
                "Source can't be equal to Destination"
            )

        return attrs
