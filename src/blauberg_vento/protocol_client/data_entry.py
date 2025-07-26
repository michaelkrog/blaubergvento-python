from dataclasses import dataclass
from typing import Optional
from src.blauberg_vento.protocol_client.parameter import Parameter  # Assuming you saved the previous enum as parameter.py


@dataclass
class DataEntry:
    """
    DataEntry class.

    Represents a single entry of data with an associated parameter and optional value.

    Attributes:
        parameter (Parameter): The parameter associated with this data entry.
        value (Optional[bytes]): The value of the data entry, represented as bytes.
    """
    parameter: Parameter
    value: Optional[bytes] = None

    def __str__(self) -> str:
        param_str = str(self.parameter.name) if hasattr(self.parameter, "name") else str(self.parameter)
        value_str = self.value.hex() if self.value is not None else "None"
        return f"DataEntry(parameter={param_str}, value={value_str})"

    @staticmethod
    def of(parameter: Parameter, value: Optional[int] = None) -> "DataEntry":
        """
        Creates a new DataEntry instance.

        Constructs a DataEntry object with a specified parameter and an optional value.
        The value is converted to a single-byte `bytes` object if provided.

        Args:
            parameter (Parameter): The parameter to associate with the data entry.
            value (Optional[int]): The value to be included in the data entry (optional).
                                   If provided, it is converted to a single-byte bytes object.

        Returns:
            DataEntry: A new DataEntry object with the given parameter and value.
        """
        return DataEntry(parameter, bytes([value]) if value is not None else None)