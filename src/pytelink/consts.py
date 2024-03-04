from enum import Enum


class NotificationOpcodes(Enum):
    """
    Opcodes for notification messages
    """

    ONLINE_STATUS = 0xDC

    # Note: these are not implemented in this library yet
    GET_GROUP = 0xD4
    GET_ALARM = 0xE7
    GET_TIME = 0xE9
    GET_DEVICE_STATE = 0xC8
    UPDATE_MESH_COMPLETE = 0xCA
    USER_ALL_NOTIFY = 0xEB
    GET_MSG_DEVICE_LIST = 0xE1


class CommandOpcodes(Enum):
    """
    Opcodes for commands
    """

    SET_ON_OFF = 0xD0
    SET_BRIGHTNESS = 0xD2
    SET_COLOR = 0xE2


class ColorType(Enum):
    """
    Type of color to set
    """

    RGB = 0x04
    TEMPERATURE = 0x05
