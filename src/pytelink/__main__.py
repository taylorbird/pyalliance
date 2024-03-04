import time
from typing import Optional, Dict
from pytelink import Controller


def main(_args: Optional[Dict[str, str]] = None) -> None:
    """
    The main routine.
    """
    controller = Controller("FF:00:05:08:0A:8B", "Back", "2846")
    controller.start()
    time.sleep(900)
