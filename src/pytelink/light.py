from dataclasses import dataclass
from typing import TYPE_CHECKING
from .consts import CommandOpcodes, ColorType
from .events import LightEvent, LightStatusEvent

if TYPE_CHECKING:
    from .controller import Controller


@dataclass
class Light:
    """
    Represents a single light in the mesh
    """

    mesh_address: int
    status: int = 0
    brightness: int = 0

    def __init__(self, controller: "Controller", mesh_address: int) -> None:
        self.controller = controller
        self.mesh_address = mesh_address

        print(f"New light: { mesh_address }")

    def is_on(self) -> bool:
        """
        Returns True if the light is on
        """
        return self.brightness > 0

    def turn_on(self) -> None:
        """
        Turn the light on
        """
        self.controller.send_light_command(self, CommandOpcodes.SET_ON_OFF, [0x01, 0x00, 0x00])

    def turn_off(self) -> None:
        """
        Turn the light off
        """
        self.controller.send_light_command(self, CommandOpcodes.SET_ON_OFF, [0x00, 0x00, 0x00])

    def set_color(self, r: int, g: int, b: int) -> None:
        """
        Set the color of the light (each value between 0-255)
        """
        self.controller.send_light_command(self, CommandOpcodes.SET_COLOR, [ColorType.RGB.value, r, g, b])

    def set_temperature(self, temp: int) -> None:
        """
        Set the temperature of the light (between 0-255)
        """
        self.controller.send_light_command(self, CommandOpcodes.SET_COLOR, [ColorType.TEMPERATURE.value, temp])

    def set_brightness(self, brightness: int) -> None:
        """
        Set the brightness of the light (between 0-100)
        """
        self.controller.send_light_command(self, CommandOpcodes.SET_BRIGHTNESS, [brightness])

    def update_from_event(self, event: LightEvent) -> None:
        """
        Updates this light's internal state from a LightEvent
        """
        if isinstance(event, LightStatusEvent):
            self._update_light_from_status_event(event)
        else:
            print(f"Unknown LightEvent: { event }")

    def _update_light_from_status_event(self, event: LightStatusEvent) -> None:
        self.brightness = event.brightness
        self.status = event.status
