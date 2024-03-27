from django.core.exceptions import ValidationError
from django.test import TestCase

from station.utils.samples import (
    sample_crew,
    sample_train_type,
    sample_train,
    sample_station,
    sample_route,
    sample_trip,
    sample_order,
    sample_ticket,
    sample_user
)


class CrewModelTest(TestCase):

    def setUp(self) -> None:
        self.crew = sample_crew()

    def test_crew_full_name(self):
        self.assertEqual(
            self.crew.full_name,
            f"{self.crew.first_name} {self.crew.last_name}"
        )

    def test_crew_str(self):
        self.assertEqual(
            str(self.crew),
            f"{self.crew.full_name} - {self.crew.position}"
        )


class TrainTypeModelTest(TestCase):

    def setUp(self) -> None:
        self.train_type = sample_train_type()

    def test_train_type_str(self):
        self.assertEqual(str(self.train_type), self.train_type.name)


class TrainModelTest(TestCase):

    def setUp(self) -> None:
        self.train = sample_train()

    def test_train_capacity(self):
        self.assertEqual(
            self.train.capacity,
            self.train.cargo_num * self.train.places_in_cargo
        )

    def test_train_str(self):
        self.assertEqual(
            str(self.train),
            f"Train: {self.train.name}. Type: {self.train.train_type}"
        )


class StationModelTest(TestCase):

    def setUp(self) -> None:
        self.station = sample_station()

    def test_station_str(self):
        self.assertEqual(
            str(self.station),
            f"Station {self.station.name} "
            f"({self.station.latitude}, {self.station.longitude})"
        )


class RouteModelTest(TestCase):

    def setUp(self) -> None:
        self.route = sample_route()

    def test_route_str(self):
        self.assertEqual(
            str(self.route),
            f"{self.route.source.name} - {self.route.destination.name}"
        )


class TripModelTest(TestCase):

    def setUp(self) -> None:
        self.trip = sample_trip()
        self.trip.crew.add(sample_crew())

    def test_trip_str(self):
        self.assertEqual(
            str(self.trip),
            f"Route: {self.trip.route}. Train: {self.trip.train.name}"
        )


class OrderModelTest(TestCase):

    def setUp(self) -> None:
        self.order = sample_order()

    def test_order_str(self):
        self.assertEqual(str(self.order), str(self.order.created_at))


class TicketModelTest(TestCase):

    def setUp(self) -> None:
        self.trip = sample_trip()
        self.ticket = sample_ticket(trip=self.trip)

    def test_validate_unique_together(self):
        order = sample_order(user=sample_user(email="user1@user.com"))

        with self.assertRaises(ValidationError):
            sample_ticket(order=order, trip=self.trip)

    def test_validate_ticket(self):
        order = sample_order(user=sample_user(email="user1@user.com"))

        with self.assertRaises(ValidationError):
            sample_ticket(
                cargo=1000,
                seat=1000,
                order=order,
                trip=self.trip
            )
