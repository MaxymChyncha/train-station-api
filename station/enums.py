from enum import Enum


class CrewPositionEnum(Enum):
    STATION_MASTER = "station_master"
    TRAIN_DRIVER = "train_driver"
    TICKET_INSPECTOR = "ticket_inspector"
    PLATFORM_ATTENDANT = "platform_attendant"
    TRAIN_DISPATCHER = "train_dispatcher"
    SECURITY_GUARD = "security_guard"
    CLEANING_STAFF = "cleaning_staff"
    OTHER = "other"
