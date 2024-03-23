from rest_framework import serializers

from station.models import Train


class TrainSerializer(serializers.ModelSerializer):

    class Meta:
        model = Train
        fields = (
            "id",
            "name",
            "cargo_num",
            "places_in_cargo",
            "train_type",
        )
