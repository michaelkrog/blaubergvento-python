from dataclasses import dataclass
from src.blauberg_vento.protocol_client.packet import Packet

@dataclass
class Response:
    """
    Response class.

    Represents a response received from a device or controller.
    """

    packet: Packet
    """The packet received in the response."""

    ip: str
    """The IP address of the device or controller that sent the response."""
