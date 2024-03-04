from typing import Any, List, Dict, Optional
from dimond import dimond

from .util import hexstring
from .light import Light
from .consts import NotificationOpcodes
from .parsers import Parsers
from .events import LightEvent
from .commands import Command, OnOffCommand, SetBrightnessCommand, SetColorCommand, SetTemperatureCommand


class Controller:
    """
    The primary telink controller
    """

    def __init__(self, mac_address: str, mesh_name: str, mesh_password: str) -> None:
        self._network = dimond(0x0211, mac_address, mesh_name, mesh_password, callback=self._dimond_callback)
        self._lights: Dict[int, Light] = {}

    def start(self) -> None:
        """
        Starts the controller, connecting to the mesh
        """
        self._network.connect()

    def lights(self) -> Dict[int, Light]:
        """
        Return a list of known lights on the network
        """
        return self._lights

    def light(self, mesh_address: int) -> Optional[Light]:
        """
        Return a specific light in the network, or None if it has not been discovered yet
        """
        return self._lights.get(mesh_address, None)

    def turn_on_all_lights(self) -> None:
        """
        Turns on all lights in the mesh
        """
        self.send_all_lights_command(OnOffCommand(True))

    def turn_off_all_lights(self) -> None:
        """
        Turns off all lights in the mesh
        """
        self.send_all_lights_command(OnOffCommand(False))

    def set_brightness_all_lights(self, brightness: int) -> None:
        """
        Sets the brightness of all lights in the mesh
        """
        self.send_all_lights_command(SetBrightnessCommand(brightness))

    def set_color_all_lights(self, r: int, g: int, b: int) -> None:
        """
        Sets the RGB color of all lights in the mesh
        """
        self.send_all_lights_command(SetColorCommand(r, g, b))

    def set_temperature_all_lights(self, temperature: int) -> None:
        """
        Sets the white temperature of all lights in the mesh
        """
        self.send_all_lights_command(SetTemperatureCommand(temperature))

    def send_light_command(self, light: Light, command: Command) -> None:
        """
        Send a command to a specific light
        """
        self._send_command(light.mesh_address, command)

    def send_all_lights_command(self, command: Command) -> None:
        """
        Send a command to all lights on the mesg
        """
        self._send_command(0xFFFF, command)

    def send_connected_light_command(self, command: Command) -> None:
        """
        Send a commands to the light we're directly connected to
        """
        self._send_command(0, command)

    def _send_command(self, mesh_address: int, command: Command) -> None:
        self._network.send_packet(mesh_address, command.opcode().value, command.serialize_params())

    def _dimond_callback(self, _mesh: Any, message: List[int]) -> None:
        # print(f"CB: { hexstring(message) }")

        _src = message[3:5]
        _vendor_id = message[8:10]
        opcode = message[7]
        data = message[10:]

        try:
            parser = Parsers[NotificationOpcodes(opcode)]
            event = parser.parse(data)
            print(f"Event: {event}")

            if isinstance(event, LightEvent):
                self._update_light_from_event(event)

        except (KeyError, ValueError):
            print(f"No parser for notification: { hexstring(message) }")

    def _update_light_from_event(self, event: LightEvent) -> None:
        address = event.mesh_address
        light = self._lights.get(address) or self._lights.setdefault(address, Light(self, address))
        light.update_from_event(event)
        print(f"Light: {light}")
