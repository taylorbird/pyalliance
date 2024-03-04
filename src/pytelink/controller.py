from typing import Any, List, Dict
from dimond import dimond

from .util import hexstring
from .light import Light
from .consts import NotificationOpcodes, CommandOpcodes
from .parsers import Parsers
from .events import LightEvent


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

    def send_light_command(self, light: Light, opcode: CommandOpcodes, params: List[int]) -> None:
        """
        Send a commands to the given light
        """
        self._network.send_packet(light.mesh_address, opcode.value, params)

    def send_all_lights_command(self, opcode: CommandOpcodes, params: List[int]) -> None:
        """
        Send a commands to all lights on the network
        """
        self._network.send_packet(0xFFFF, opcode.value, params)

    def send_connected_light_command(self, opcode: CommandOpcodes, params: List[int]) -> None:
        """
        Send a commands to the light we're directly connected to
        """
        self._network.send_packet(0, opcode.value, params)

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
