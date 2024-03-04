from dataclasses import dataclass
from typing import TYPE_CHECKING
from .consts import CommandOpcodes, ColorType
from .events import LightEvent, LightStatusEvent
from .commands import OnOffCommand, SetBrightnessCommand, SetColorCommand, SetTemperatureCommand

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
        Turns on the light
        """
        self.controller.send_light_command(self, OnOffCommand(True))

    def turn_off(self) -> None:
        """
        Turns off the light
        """
        self.controller.send_light_command(self, OnOffCommand(False))

    def set_brightness(self, brightness: int) -> None:
        """
        Sets the brightness of the light
        """
        self.controller.send_light_command(self, SetBrightnessCommand(brightness))

    def set_color(self, r: int, g: int, b: int) -> None:
        """
        Sets the RGB color of the light
        """
        self.controller.send_light_command(self, SetColorCommand(r, g, b))

    def set_temperature_all_lights(self, temperature: int) -> None:
        """
        Sets the white temperature of the light
        """
        self.controller.send_light_command(self, SetTemperatureCommand(temperature))

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
