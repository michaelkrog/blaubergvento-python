from enum import IntEnum

class Mode(IntEnum):
    """
    Enum representing the directions available for a device.

    The direction can be configured by the device's dip switch.
    """

    ONEWAY = 0  # One-way direction (set based on the dip switch on the device)
    TWOWAY = 1  # Two-way direction
    IN = 2      # Inward direction
