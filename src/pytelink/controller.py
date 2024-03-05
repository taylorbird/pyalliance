from typing import Any, List, Dict, Optional
from dimond import dimond

from .util import hexstring
from .light import Light
from .consts import NotificationOpcodes
from .parsers import Parsers
from .events import LightEvent
from .commands import Command


class Controller:
    """
    The primary telink controller
    """

    def __init__(self, mac_address: str, mesh_name: str, mesh_password: str) -> None:
        self._network = dimond(
            0x0211, mac_address, mesh_name, mesh_password, callback=self._dimond_callback, auto_notifications=False
        )
        self._lights: Dict[int, Light] = {}
        self._all_lights = Light(self, 0xFFFF)

    def start(self) -> None:
        """
        Starts the controller, connecting to the mesh
        """
        self._network.connect()

    def process_notifications(self, timeout: float) -> None:
        """
        Process any pending notifications
        """
        self._network.process_notifications(timeout)

    def lights(self) -> Dict[int, Light]:
        """
        Return a list of known lights on the network
        """
        return self._lights

    def all(self) -> Light:
        """
        Returns a psuedo Light that can be used to control all lights on the mesh at once
        """
        return self._all_lights

    def light(self, mesh_address: int) -> Optional[Light]:
        """
        Return a specific light in the network, or None if it has not been discovered yet
        """
        # return self._lights.get(mesh_address, None)
        return self._get_or_create_light(mesh_address)

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
            # print(f"Event: {event}")

            if isinstance(event, LightEvent):
                self._update_light_from_event(event)

        except (KeyError, ValueError):
            print(f"No parser for notification: { hexstring(message) }")

    def _get_or_create_light(self, address: int) -> Light:
        return self._lights.get(address) or self._lights.setdefault(address, Light(self, address))

    def _update_light_from_event(self, event: LightEvent) -> None:
        light = self._get_or_create_light(event.mesh_address)
        light.update_from_event(event)
        # print(f"Light: {light}")
