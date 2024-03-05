from typing import Optional, Dict, List, Tuple
import sacn

from pytelink import Controller


def main(_args: Optional[Dict[str, str]] = None) -> None:
    """
    The main routine.
    """

    print("Starting Controller")
    controller = Controller("FF:00:05:08:0A:8B", "Back", "2846")
    controller.start()

    # Allow some time to find all the lights
    print("Discovering lights")
    controller.process_notifications(5)

    lights = list(controller.lights().values())
    lights.sort(key=lambda item: item.mesh_address)
    print(f"Found {len(lights)} lights")

    controller.all().turn_on()
    controller.all().set_color(255, 255, 255)

    print("Starting sACN receiver")

    receiver = sacn.sACNreceiver()
    receiver.start()
    receiver.join_multicast(1)

    colors: List[Tuple[int, ...]] = []

    @receiver.listen_on("universe", universe=1)
    def callback(packet: sacn.DataPacket) -> None:
        # print(packet.dmxData)
        nonlocal colors
        data = packet.dmxData
        colors = [data[x : x + 3] for x in range(0, len(data), 3)]
        colors = colors[0 : len(lights)]
        # print(colors)
        print("Packet")

    while True:
        print("Loop")

        for i, [r, g, b] in enumerate(colors):
            print(f"Set {i} to RGB {r} {g} {b} ({lights[i]})")
            lights[i].set_color(r, g, b)

        print("Loop Done")
        controller.process_notifications(0.050)
