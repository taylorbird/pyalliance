from dataclasses import dataclass


@dataclass
class Event:
    """
    Base event class
    """


@dataclass
class LightEvent(Event):
    """
    An event related to a specific light
    """

    mesh_address: int


@dataclass
class LightStatusEvent(LightEvent):
    """
    Event for when a light's status is updated
    """

    status: int
    brightness: int
