from typing import Any, List, Dict
from dimond import dimond
from .util import hexstring
from .light import Light


class Controller:
    """
    The primary telink controller
    """

    def __init__(self) -> None:
        self.network = dimond(0x0211, "FF:00:05:08:0A:8B", "Back", "2846", callback=self.dimond_callback)
        self.lights: Dict[int, Light] = dict()

    def start(self) -> None:
        """
        Starts the controller, connecting to the mesh
        """
        self.network.connect()

    def dimond_callback(self, _mesh: Any, message: List[int]) -> None:
        """
        Nothing
        """
        print(f"CB: { hexstring(message) }")

        opcode = message[7]
        data = message[10:]

        if opcode == 0xDC:
            mesh_address, status, brightness = data[0:3]
            print(f"Light: {mesh_address} {status} {brightness}")
