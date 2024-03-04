from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from .consts import ColorType, CommandOpcodes


@dataclass
class Command(ABC):
    """
    Base command class
    """

    @abstractmethod
    def opcode(self) -> CommandOpcodes:
        """
        Returns the opcode for this command
        """

    @abstractmethod
    def serialize_params(self) -> List[int]:
        """
        Returns the serialized params for this command
        """


@dataclass
class OnOffCommand(Command):
    """
    A command to turn lights on/off
    """

    on: bool

    def opcode(self) -> CommandOpcodes:
        return CommandOpcodes.SET_ON_OFF

    def serialize_params(self) -> List[int]:
        return [0x01 if self.on else 0x00, 0x00, 0x00]


@dataclass
class SetBrightnessCommand(Command):
    """
    A command to set brightness
    """

    brightness: int

    def opcode(self) -> CommandOpcodes:
        return CommandOpcodes.SET_BRIGHTNESS

    def serialize_params(self) -> List[int]:
        return [self.brightness]


@dataclass
class SetColorCommand(Command):
    """
    A command to set rgb color
    """

    r: int
    g: int
    b: int

    def opcode(self) -> CommandOpcodes:
        return CommandOpcodes.SET_COLOR

    def serialize_params(self) -> List[int]:
        return [ColorType.RGB.value, self.r, self.g, self.b]


@dataclass
class SetTemperatureCommand(Command):
    """
    A command to set white color temperature
    """

    temperature: int

    def opcode(self) -> CommandOpcodes:
        return CommandOpcodes.SET_COLOR

    def serialize_params(self) -> List[int]:
        return [ColorType.TEMPERATURE.value, self.temperature]
