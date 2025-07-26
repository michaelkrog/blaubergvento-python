from datetime import datetime
from typing import Optional

from src.blauberg_vento.protocol_client.data_entry import DataEntry
from src.blauberg_vento.protocol_client.function_type import FunctionType
from src.blauberg_vento.protocol_client.packet import Packet
from src.blauberg_vento.protocol_client.parameter import Parameter
from mode import Mode
from speed import Speed


class Device:
    """
    A class representing a single Duke One Device.

    This class provides methods to serialize and deserialize device state
    from and to `Packet` instances, and to manage device-specific properties.
    """

    def __init__(self, device_id: str, password: str):
        """
        Creates an instance of the Device class.

        :param device_id: The unique identifier for the device.
        :param password: The password for the device.
        """
        self.id: str = device_id
        self.password: str = password

        self.speed: Optional[Speed] = None
        self.mode: Optional[Mode] = None
        self.manual_speed: Optional[int] = None
        self.fan1_rpm: Optional[int] = None
        self.humidity: Optional[int] = None
        self.filter_alarm: bool = False
        self.filter_time: Optional[int] = None
        self.on: bool = False
        self.firmware_version: Optional[str] = None
        self.firmware_date: Optional[datetime] = None
        self.unit_type: Optional[int] = None
        self.ip_address: Optional[str] = None

    def to_packet(self) -> Packet:
        """
        Converts the device state to a `Packet` for communication.

        :return: Packet containing the device's current state.
        """
        data_entries = [
            DataEntry.of(Parameter.SPEED, self.speed),
            DataEntry.of(Parameter.VENTILATION_MODE, self.mode),
            DataEntry.of(Parameter.MANUAL_SPEED, self.manual_speed),
            DataEntry.of(Parameter.ON_OFF, 1 if self.on else 0),
        ]
        return Packet(self.id, self.password, FunctionType.WRITEREAD, data_entries)

    @staticmethod
    def from_packet(packet: Packet) -> "Device":
        """
        Creates a Device instance from a Packet.

        :param packet: The packet containing device data.
        :return: Device instance populated from the packet.
        """
        device = Device(packet.device_id, packet.password)
        for entry in packet.data_entries:
            Device.apply_parameter(device, entry)
        return device

    @staticmethod
    def apply_parameter(device: "Device", data_entry: DataEntry):
        """
        Applies a DataEntry to a Device instance, updating its properties.

        :param device: Device to update.
        :param data_entry: DataEntry containing the parameter and value.
        """
        p = data_entry.parameter
        v = data_entry.value

        if p == Parameter.CURRENT_HUMIDITY:
            device.humidity = v[0]
        elif p == Parameter.VENTILATION_MODE:
            device.mode = v[0]
        elif p == Parameter.FAN1RPM:
            device.fan1_rpm = v[0] + (v[1] << 8)
        elif p == Parameter.FILTER_ALARM:
            device.filter_alarm = v[0] == 1
        elif p == Parameter.FILTER_TIMER:
            device.filter_time = v[0] + (v[2] * 24 + v[1]) * 60
        elif p == Parameter.CURRENT_IP_ADDRESS:
            device.ip_address = f"{v[0]}.{v[1]}.{v[2]}.{v[3]}"
        elif p == Parameter.MANUAL_SPEED:
            device.manual_speed = v[0]
        elif p == Parameter.SPEED:
            device.speed = v[0]
        elif p == Parameter.ON_OFF:
            device.on = v[0] == 1
        elif p == Parameter.READ_FIRMWARE_VERSION:
            major, minor, day, month, year_low, year_high = v
            year = year_low + (year_high << 8)
            device.firmware_version = f"{major}.{minor}"
            device.firmware_date = datetime(year, month, day)
        elif p == Parameter.UNIT_TYPE:
            device.unit_type = v[0]
