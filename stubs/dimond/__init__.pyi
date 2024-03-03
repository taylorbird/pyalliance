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
    ) -> None: ...
    def connect(self) -> None: ...
