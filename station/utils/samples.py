import datetime

from django.contrib.auth import get_user_model

from station.models import (
    Crew,
    TrainType,
    Train,
    Station,
    Route,
    Trip,
    Order,
    Ticket
)


def sample_superuser(**params):
    defaults = {
        "email": "admin@admin.com",
        "password": "test1234",
        "first_name": "admin_first_name",
        "last_name": "admin_last_name"
    }
    defaults.update(params)

    return get_user_model().objects.create_superuser(**defaults)


def sample_user(**params):
    defaults = {
        "email": "user@user.com",
        "password": "test1234",
        "first_name": "user_first_name",
        "last_name": "user_last_name"
    }
    defaults.update(params)

    return get_user_model().objects.create_user(**defaults)


def sample_crew(**params):
    defaults = {
        "first_name": "crew_first_name",
        "last_name": "crew_last_name",
        "position": "other"
    }
    defaults.update(params)

    return Crew.objects.create(**defaults)


def sample_train_type(**params):
    defaults = {"name": "train_type_name"}
    defaults.update(params)

    return TrainType.objects.create(**defaults)


def sample_train(**params):
    train_type = sample_train_type()

    defaults = {
        "name": "train_name",
        "cargo_num": 10,
        "places_in_cargo": 20,
        "train_type": train_type
    }
    defaults.update(params)

    return Train.objects.create(**defaults)


def sample_station(**params):
    defaults = {
        "name": "station_name",
        "latitude": 4.0,
        "longitude": 2.5
    }
    defaults.update(params)

    return Station.objects.create(**defaults)


def sample_route(**params):
    source = sample_station()
    destination = sample_station(
        name="destination", latitude=1.0, longitude=5.0
    )

    defaults = {
        "source": source,
        "destination": destination,
        "distance": 150
    }
    defaults.update(params)

    return Route.objects.create(**defaults)


def sample_trip(**params):
    route = sample_route()
    train = sample_train()

    defaults = {
        "route": route,
        "train": train,
        "departure_time": datetime.datetime(
            year=2024,
            month=4,
            day=1,
            hour=12,
            minute=30
        ),
        "arrival_time": datetime.datetime(
            year=2024,
            month=4,
            day=2,
            hour=18,
            minute=30
        )
    }
    defaults.update(params)

    return Trip.objects.create(**defaults)


def sample_order(**params):
    # user = params.get("user", sample_user())
    if not params.get("user"):
        user = sample_user()
    else:
        user = params.get("user")

    defaults = {"user": user}
    defaults.update(params)

    return Order.objects.create(**defaults)


def sample_ticket(**params):
    trip = params.get("trip", sample_trip())
    # order = params.get("order", sample_order())
    if not params.get("order"):
        order = sample_order()
    else:
        order = params.get("order")

    defaults = {
        "cargo": 1,
        "seat": 1,
        "trip": trip,
        "order": order
    }
    defaults.update(params)

    return Ticket.objects.create(**defaults)
