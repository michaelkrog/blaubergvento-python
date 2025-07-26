from enum import Enum

class FunctionType(Enum):
    """
    FunctionType enumeration.

    This enum defines the different types of functions that can be used in communication protocols.
    Each type is represented by a unique byte value.
    """

    READ = 0x01
    """Indicates a request to read data from a device or controller."""

    WRITE = 0x02
    """Indicates a request to write data to a device or controller."""

    WRITEREAD = 0x03
    """Indicates a request to both write data to and read data from a device or controller."""

    INCREAD = 0x04
    """Indicates a request to increment a value on a device or controller and read the result."""

    DECREAD = 0x05
    """Indicates a request to decrement a value on a device or controller and read the result."""

    RESPONSE = 0x06
    """Indicates a response from a device or controller to a request."""
