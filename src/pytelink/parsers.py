from abc import ABC, abstractmethod
from typing import List
from .consts import NotificationOpcodes
from .events import Event, LightStatusEvent


class NotificationParser(ABC):
    """
    Parses notifications
    """

    @abstractmethod
    def parse(self, message: List[int]) -> Event:
        """
        Parses the given notification and returns an event object
        """


class OnlineStatusParser(NotificationParser):
    """
    Parses ONLINE_STATUS messages
    """

    def parse(self, message: List[int]) -> LightStatusEvent:
        return LightStatusEvent(mesh_address=message[0], status=message[1], brightness=message[2])


Parsers = {NotificationOpcodes.ONLINE_STATUS: OnlineStatusParser()}
