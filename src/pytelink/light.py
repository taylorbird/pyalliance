from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .controller import Controller


class Light:
    """
    Represents a single light in the mesh
    """

    def __init__(self, controller: "Controller", mesh_address: int) -> None:
        self.controller = controller
        self.mesh_address = mesh_address
        print(f"NL: { mesh_address }")
