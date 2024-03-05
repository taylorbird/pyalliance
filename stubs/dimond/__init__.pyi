# pylint: skip-file

from typing import Callable, Optional, Any, List

class dimond:
    def __init__(
        self,
        vendor: int,
        mac: str,
        name: str,
        password: str,
        mesh: Optional[Any] = None,
        callback: Optional[Callable[[Any, List[int]], None]] = None,
        auto_notifications: bool = False,
    ) -> None: ...
    def connect(self) -> None: ...
    def send_packet(self, target: int, command: int, data: List[int]) -> None: ...
    def process_notifications(self, timeout: float) -> None: ...
