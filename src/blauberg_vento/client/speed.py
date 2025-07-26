from enum import IntEnum

class Speed(IntEnum):
    """
    Enum representing the speed options available for a device.
    """

    OFF = 0      # The device is turned off
    LOW = 1      # The device is set to low speed
    MEDIUM = 2   # The device is set to medium speed
    HIGH = 3     # The device is set to high speed
    MANUAL = 255 # The device is set to manual speed (controlled manually)
