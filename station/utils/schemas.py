from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
)


def trip_list_schema():
    return extend_schema(
        description=(
            "Endpoint for up to date representation list of trips "
            "with possibility to filtering by location, "
            "departure and arrival date."
        ),
        parameters=[
            OpenApiParameter(
                "from",
                type=OpenApiTypes.STR,
                description="Filter by from location (source)",
                examples=[
                    OpenApiExample(name="Example 1", value="Central Station")
                ]
            ),
            OpenApiParameter(
                "to",
                type=OpenApiTypes.STR,
                description="Filter by to location (destination)",
                examples=[
                    OpenApiExample(name="Example 1", value="Union Station")
                ]
            ),
            OpenApiParameter(
                "departure_time",
                type=OpenApiTypes.DATE,
                description="Filter by to departure date",
                examples=[
                    OpenApiExample(name="Example 1", value="2024-04-01")
                ]
            ),
            OpenApiParameter(
                "arrival_time",
                type=OpenApiTypes.DATE,
                description="Filter by to arrival date",
                examples=[
                    OpenApiExample(name="Example 1", value="2024-04-02")
                ]
            ),
        ]
    )


def route_list_schema():
    return extend_schema(
        description=(
            "Endpoint for representation list of routes "
            "with possibility to filtering by source and destination."
        ),
        parameters=[
            OpenApiParameter(
                "source",
                type=OpenApiTypes.STR,
                description="Filter by source",
                examples=[
                    OpenApiExample(name="Example 1", value="Central Station")
                ]
            ),
            OpenApiParameter(
                "destination",
                type=OpenApiTypes.STR,
                description="Filter by destination",
                examples=[
                    OpenApiExample(name="Example 1", value="Union Station")
                ]
            ),
        ]
    )
