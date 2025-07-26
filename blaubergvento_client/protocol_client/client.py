import socket
import time
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from blaubergvento_client.protocol_client.packet import Packet
from blaubergvento_client.protocol_client.function_type import FunctionType
from blaubergvento_client.protocol_client.data_entry import DataEntry
from blaubergvento_client.protocol_client.parameter import Parameter
from blaubergvento_client.protocol_client.response import Response

TIME_OUT = 1.0

BROADCAST_ADDRESS = "255.255.255.255"
DEFAULT_TIMEOUT = 0.3  # seconds


@dataclass
class DeviceAddress:
    """
    Represents the structure of a discovered device's address information.

    Attributes:
        id (str): The unique identifier of the device.
        ip (str): The IP address of the discovered device.
    """
    id: str
    ip: str


class ProtocolClient:
    """
    This class provides methods to discover Blauberg Vento devices on the local network
    and to communicate with specific controllers via UDP.
    """

    def __init__(self, timeout: float = DEFAULT_TIMEOUT):
        self.timeout = timeout

    async def find_devices(self) -> List[DeviceAddress]:
        """
        Find devices on the network by emitting a broadcast packet and collecting all answering controllers.

        Returns:
            List[DeviceAddress]: List of discovered devices.
        """
        devices: List[DeviceAddress] = []
        last_response_time = datetime.now()

        # Build the search packet
        packet = Packet(
            device_id="DEFAULT_DEVICEID",
            password="",
            function_type=FunctionType.READ,
            data_entries=[DataEntry.of(Parameter.SEARCH)]
        )


        # Create UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(TIME_OUT)

        # Start listening
        sock.bind(('', 0))

        # Send the broadcast packet
        sock.sendto(packet.to_bytes(), (BROADCAST_ADDRESS, 4000))

        # Listen for replies (on the ephemeral port)
        start_time = time.time()
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                packet = Packet.from_bytes(data)
                devices.append(DeviceAddress(id= packet.device_id, ip=addr[0]))
                print(f"Received reply from {addr}: {packet}")
            except socket.timeout:
                break
            if time.time() - start_time > 1:
                break

        sock.close()

        return devices

    async def send(self, packet: Packet, ip: str = BROADCAST_ADDRESS) -> Optional[Response]:
        """
        Sends a packet to a specific controller.

        Args:
            packet (Packet): The packet to send.
            ip (str): The IP address of the controller (default is broadcast).

        Returns:
            Response | None: The response packet, or None if no response is received.
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setblocking(True)
        sock.settimeout(1.0)

        # Send packet
        sock.sendto(packet.to_bytes(), (ip, 4000))

        try:
            data, addr = sock.recvfrom(1024)
            received_packet = Packet.from_bytes(data)
            if received_packet.function_type == FunctionType.RESPONSE:
                return Response(packet=received_packet, ip=addr[0])
        finally:
            sock.close()
