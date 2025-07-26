from typing import Optional, Dict

from blaubergvento_client.client.device import Device
from blaubergvento_client.protocol_client.client import ProtocolClient
from blaubergvento_client.protocol_client.data_entry import DataEntry
from blaubergvento_client.protocol_client.function_type import FunctionType
from blaubergvento_client.protocol_client.packet import Packet
from blaubergvento_client.protocol_client.parameter import Parameter


class Client:
    def __init__(self):
        self.client = ProtocolClient()
        self._ip_map: Optional[Dict[str, str]] = None

    async def find_all(self, page: int = 0, size: int = 20) -> list[Device]:
        ip_map = await self._resolve_ip_map()
        device_addresses = list(ip_map.items())

        start = page * size
        end = start + size
        device_addresses = device_addresses[start:end]

        devices = []
        for device_id, ip in device_addresses:
            device = await self._resolve_device(device_id, ip)
            if device:
                devices.append(device)

        return devices

    async def find_by_id(self, device_id: str) -> Optional[Device]:
        ip = (await self._resolve_ip_map()).get(device_id)
        return await self._resolve_device(device_id, ip)

    async def save(self, entity: Device) -> Optional[Device]:
        ip = (await self._resolve_ip_map()).get(entity.id)
        response = await self.client.send(entity.to_packet(), ip)
        return Device.from_packet(response.packet) if response else None

    async def _resolve_device(self, device_id: str, ip: str) -> Optional[Device]:
        packet = Packet(
            device_id,
            "1111",
            FunctionType.READ,
            [
                DataEntry.of(Parameter.ON_OFF),
                DataEntry.of(Parameter.VENTILATION_MODE),
                DataEntry.of(Parameter.SPEED),
                DataEntry.of(Parameter.MANUAL_SPEED),
                DataEntry.of(Parameter.FAN1RPM),
                DataEntry.of(Parameter.FILTER_ALARM),
                DataEntry.of(Parameter.FILTER_TIMER),
                DataEntry.of(Parameter.CURRENT_HUMIDITY),
                DataEntry.of(Parameter.READ_FIRMWARE_VERSION),
                DataEntry.of(Parameter.CURRENT_IP_ADDRESS)
            ]
        )
        response = await self.client.send(packet, ip)
        return Device.from_packet(response.packet) if response else None

    async def _resolve_ip_map(self) -> Dict[str, str]:
        if self._ip_map is None:
            self._ip_map = {}
            addresses = await self.client.find_devices()
            for addr in addresses:
                self._ip_map[addr.id] = addr.ip
        return self._ip_map