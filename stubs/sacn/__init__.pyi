# pylint: skip-file

from typing import Any, Optional, Callable, overload, Literal, TypeVar, Tuple

class ReceiverSocketBase: ...
class ReceiverHandlerListener: ...

ListenOnCallback = TypeVar("ListenOnCallback", bound=Callable[[DataPacket], None])

class sACNreceiver(ReceiverHandlerListener):
    def __init__(
        self, bind_address: str = "0.0.0.0", bind_port: int = 5568, socket: Optional[ReceiverSocketBase] = None
    ): ...
    def start(self) -> None: ...
    def join_multicast(self, universe: int) -> None: ...
    @overload
    def listen_on(
        self, trigger: Literal["universe"], universe: int
    ) -> Callable[[Callable[[DataPacket], None]], None]: ...
    @overload
    def listen_on(self, trigger: Literal["availability"]) -> Callable[[Callable[[int, str], None]], None]: ...

class RootLayer:
    length: int
    cid: Tuple[Any]
    vector: Tuple[Any]

class DataPacket(RootLayer):
    sourceName: str
    priority: int
    syncAddr: int
    universe: int
    option_StreamTerminated: bool
    option_PreviewData: bool
    option_ForceSync: bool
    sequence: int
    dmxStartCode: int
    dmxData: Tuple[int, ...]
