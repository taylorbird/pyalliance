import time
from typing import Optional, Dict
from pytelink import Controller


def main(_args: Optional[Dict[str, str]] = None) -> None:
    """
    The main routine.
    """
    controller = Controller()
    controller.start()
    time.sleep(900)
