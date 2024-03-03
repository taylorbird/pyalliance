from typing import List


def hexstring(values: List[int]) -> str:
    """
    Converts a List of ints to a hex string
    """
    return " ".join([f"{x:02X}" for x in values])
