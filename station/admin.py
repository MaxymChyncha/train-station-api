from django.contrib import admin

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

admin.site.register(Crew)
admin.site.register(TrainType)
admin.site.register(Station)


class TicketInLine(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketInLine,)


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("train_type")
        return queryset


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("source", "destination")
        return queryset


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related(
            "route__source",
            "route__destination",
            "train"
        )
        return queryset
