from typing import List, Tuple
from src.blauberg_vento.protocol_client.data_entry import DataEntry
from src.blauberg_vento.protocol_client.function_type import FunctionType
from src.blauberg_vento.protocol_client.parameter import Parameter, get_size

MAX_PACKET_SIZE = 256
HEADER = [0xFD, 0xFD]
PROTOCOL_TYPE = 0x02


class Packet:
    """
    Packet class.

    Represents a communication packet used in the protocol. The packet includes headers, credentials,
    function types, data entries, and a checksum to ensure data integrity.
    """

    def __init__(self, device_id: str, password: str, function_type: FunctionType, data_entries: List[DataEntry]):
        """
        Creates a new Packet instance.

        :param device_id: The device ID to include in the packet.
        :param password: The password for the device.
        :param function_type: The type of function to perform.
        :param data_entries: The data entries to include in the packet.
        """
        self._device_id = device_id
        self._password = password
        self._function_type = function_type
        self._data_entries = data_entries

    @property
    def device_id(self) -> str:
        """Gets the device ID."""
        return self._device_id

    @property
    def password(self) -> str:
        """Gets the password."""
        return self._password

    @property
    def function_type(self) -> FunctionType:
        """Gets the function type."""
        return self._function_type

    @property
    def data_entries(self) -> List[DataEntry]:
        """Gets the data entries."""
        return self._data_entries

    def to_bytes(self) -> bytes:
        """
        Serializes the packet to a byte array.

        The packet is serialized into a byte array with a specific format including a header, protocol type,
        credentials, function type, data entries, and a checksum.

        :return: The serialized byte array of the packet.
        """
        bytes_arr = bytearray(MAX_PACKET_SIZE)
        index = 0

        # Header
        bytes_arr[index] = HEADER[0]
        index += 1
        bytes_arr[index] = HEADER[1]
        index += 1

        # Protocol Type
        bytes_arr[index] = PROTOCOL_TYPE
        index += 1

        # Credentials
        index = self._write_credential(bytes_arr, index, self._device_id)
        index = self._write_credential(bytes_arr, index, self._password)

        # Function
        bytes_arr[index] = self._function_type.value
        index += 1

        # Data
        for e in self._data_entries:
            bytes_arr[index] = e.parameter
            index += 1
            if e.value is not None and self.function_type in (FunctionType.WRITE, FunctionType.WRITEREAD):
                size = get_size(e.parameter)
                for i in range(size):
                    bytes_arr[index] = e.value[i]
                    index += 1

        # CRC
        checksum = Packet._calculate_checksum(bytes_arr[2:index])
        bytes_arr[index] = checksum & 0xFF
        index += 1
        bytes_arr[index] = (checksum >> 8) & 0xFF
        index += 1

        # Trim
        return bytes(bytes_arr[:index])

    @staticmethod
    def from_bytes(bytes_arr: bytes) -> "Packet":
        """
        Deserializes a byte array into a Packet instance.

        :param bytes_arr: The byte array to deserialize.
        :return: The deserialized Packet instance.
        :raises ValueError: If the header, protocol type, or checksum are invalid.
        """
        index = 0

        # Header
        if bytes_arr[index] != HEADER[0] or bytes_arr[index + 1] != HEADER[1]:
            raise ValueError("Invalid header.")
        index += 2

        # Protocol Type
        protocol_type = bytes_arr[index]
        if protocol_type != PROTOCOL_TYPE:
            raise ValueError("Invalid protocol type.")
        index += 1

        # Checksum
        checksum = Packet._calculate_checksum(bytes_arr[2:-2])
        data_checksum = bytes_arr[-2] + (bytes_arr[-1] << 8)
        if checksum != data_checksum:
            raise ValueError("Invalid checksum.")

        # Controller ID
        controller_id, index = Packet._read_credential(bytes_arr, index)

        # Password
        password, index = Packet._read_credential(bytes_arr, index)

        # Function
        function_type = FunctionType(bytes_arr[index])
        index += 1

        # Data
        data_entries, _ = Packet._read_parameters(bytes_arr, index)

        return Packet(controller_id, password, function_type, data_entries)

    @staticmethod
    def _read_credential(bytes_arr: bytes, index: int) -> Tuple[str, int]:
        """
        Reads a credential from the byte array.

        :param bytes_arr: The byte array containing the credential.
        :param index: The starting index to read from.
        :return: A tuple containing the credential string and the next index.
        """
        credential_size = bytes_arr[index]
        index += 1
        credential = ''.join(chr(bytes_arr[index + i]) for i in range(credential_size))
        index += credential_size
        return credential, index

    def _write_credential(self, bytes_arr: bytearray, index: int, value: str) -> int:
        """
        Writes a credential to the byte array.

        :param bytes_arr: The byte array to write to.
        :param index: The starting index to write at.
        :param value: The credential to write.
        :return: The next index after writing the credential.
        """
        bytes_arr[index] = len(value)
        index += 1
        for char in value:
            bytes_arr[index] = ord(char)
            index += 1
        return index

    def __str__(self) -> str:
        entries_str = ', '.join(str(e) for e in self._data_entries)
        return (
            f"Packet(\n"
            f"  device_id='{self._device_id}',\n"
            f"  password='{self._password}',\n"
            f"  function_type={self._function_type},\n"
            f"  data_entries=[{entries_str}]\n"
            f")"
        )

    @staticmethod
    def _read_parameters(bytes_arr: bytes, index: int) -> Tuple[List[DataEntry], int]:
        """
        Reads data entries (parameters and values) from the byte array.

        :param bytes_arr: The byte array containing the data entries.
        :param index: The starting index to read from.
        :return: A tuple containing the array of DataEntry objects and the next index.
        """
        entries = []
        while index < len(bytes_arr) - 3:
            parameter = bytes_arr[index]
            index += 1
            size = 1
            if parameter == 0xFE:
                size = bytes_arr[index]
                index += 1
                parameter = bytes_arr[index]
                index += 1
            else:
                size = get_size(Parameter(parameter))
                if size < 0:
                    raise ValueError(f"Invalid parameter [param={parameter}]")

            value = None
            if size > 0:
                value = bytes_arr[index:index + size]
                index += size
            entries.append(DataEntry(parameter, value))
        return entries, index

    @staticmethod
    def _calculate_checksum(bytes_arr: bytes) -> int:
        """
        Calculates the checksum for a byte array.

        :param bytes_arr: The byte array to calculate the checksum for.
        :return: The calculated checksum.
        """
        return sum(bytes_arr) & 0xFFFF
