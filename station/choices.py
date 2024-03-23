from station.enums import CrewPositionEnum

CREW_POSITION_TYPE = (
    (CrewPositionEnum.STATION_MASTER.value, "Master Station"),
    (CrewPositionEnum.TRAIN_DRIVER.value, "Train Driver"),
    (CrewPositionEnum.TICKET_INSPECTOR.value, "Ticket Inspector"),
    (CrewPositionEnum.PLATFORM_ATTENDANT.value, "Platform Attendant"),
    (CrewPositionEnum.TRAIN_DISPATCHER.value, "Train Dispatcher"),
    (CrewPositionEnum.SECURITY_GUARD.value, "Security Guard"),
    (CrewPositionEnum.CLEANING_STAFF.value, "Cleaning Staff"),
    (CrewPositionEnum.OTHER.value, "Other"),
)
