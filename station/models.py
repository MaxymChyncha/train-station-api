from django.contrib.auth import get_user_model
from django.db import models

from station.choices import CREW_POSITION_TYPE


class Crew(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    position = models.CharField(max_length=63, choices=CREW_POSITION_TYPE)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name} - {self.position}"


class TrainType(models.Model):
    name = models.CharField(max_length=63)

    class Meta:
        verbose_name = "Train Type"
        verbose_name_plural = "Train Types"

    def __str__(self) -> str:
        return self.name


class Train(models.Model):
    name = models.CharField(max_length=63)
    cargo_num = models.PositiveIntegerField()
    places_in_cargo = models.PositiveIntegerField()
    train_type = models.ForeignKey(
        to=TrainType,
        on_delete=models.PROTECT,
        related_name="trains"
    )

    def __str__(self) -> str:
        return f"Train: {self.name}. Type: {self.train_type}"


class Station(models.Model):
    name = models.CharField(max_length=63)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self) -> str:
        return f"Station {self.name} ({self.latitude}, {self.longitude})"


class Route(models.Model):
    source = models.ForeignKey(
        to=Station,
        on_delete=models.CASCADE,
        related_name="source_routes"
    )
    destination = models.ForeignKey(
        to=Station,
        on_delete=models.CASCADE,
        related_name="destination_routes"
    )
    distance = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.source.name} - {self.destination.name}"


class Trip(models.Model):
    route = models.ForeignKey(
        to=Route,
        on_delete=models.CASCADE,
        related_name="trips"
    )
    train = models.ForeignKey(
        to=Train,
        on_delete=models.CASCADE,
        related_name="trips"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self) -> str:
        return f"Route: {self.route}. Train: {self.train.name}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="orders"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.created_at)


class Ticket(models.Model):
    cargo = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    trip = models.ForeignKey(
        to=Trip,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    class Meta:
        unique_together = ("trip", "cargo", "seat")
        ordering = ["cargo", "seat"]

    def __str__(self) -> str:
        return (
            f"{self.trip} (cargo: {self.cargo}, seat: {self.seat})"
        )
