from enum import IntEnum

class Parameter(IntEnum):
    """ 
    Parameter enumeration.

    This enum defines various parameters used in communication with devices or controllers.
    Each parameter is associated with a unique byte value that represents a specific setting or state.
    """
    ON_OFF = 0x01
    SPEED = 0x02
    BOOT_MODE = 0x06
    TIMER_MODE = 0x07
    TIMER_COUNT_DOWN = 0x08
    HUMIDITY_SENSOR_ACTIVATION = 0x0F
    RELAY_SENSOR_ACTIVIATION = 0x14
    VOLTAGE_SENSOR_ACTIVATION = 0x16  # 0-10V
    HUMIDITY_THRESHOLD = 0x19
    CURRENT_RTC_BATTERY_VOLTAGE = 0x24  # 0-5000mv
    CURRENT_HUMIDITY = 0x25
    CURRENT_VOLTAGE_SENSOR_STATE = 0x2D  # 0-100
    CURRENT_RELAY_SENSOR_STATE = 0x32
    MANUAL_SPEED = 0x44
    FAN1RPM = 0x4A
    FAN2RPM = 0x4B
    FILTER_TIMER = 0x64
    RESET_FILTER_TIMER = 0x65
    BOOST_MODE_DEACTIVATION_DELAY = 0x66  # 0-60 minutes
    RTC_TIME = 0x6F
    RTC_CALENDAR = 0x70
    WEEKLY_SCHEDULE = 0x72
    SCHEDULE_SETUP = 0x77
    SEARCH = 0x7C
    PASSWORD = 0x7D
    MACHINE_HOURS = 0x7E
    RESET_ALARMS = 0x80
    READ_ALARM = 0x83
    CLOUD_SERVER_OPERATION_PERMISSION = 0x85
    READ_FIRMWARE_VERSION = 0x86
    RESTORE_FACTORY_SETTINGS = 0x87
    FILTER_ALARM = 0x88
    WIFI_MODE = 0x94
    WIFI_NAME = 0x95
    WIFI_PASSWORD = 0x96
    WIFI_ENCRYPTION = 0x99
    WIFI_CHANNEL = 0x9A
    WIFI_DHCP = 0x9B
    IP_ADDRESS = 0x9C
    SUBNET_MASK = 0x9D
    GATEWAY = 0x9E
    CURRENT_IP_ADDRESS = 0xA3
    VENTILATION_MODE = 0xB7
    UNIT_TYPE = 0xB9


# Parameter details with size information (converted to a dictionary for fast lookup)
details = {
    Parameter.ON_OFF: 1,
    Parameter.SPEED: 1,
    Parameter.BOOT_MODE: 1,
    Parameter.TIMER_MODE: 1,
    Parameter.TIMER_COUNT_DOWN: 3,
    Parameter.HUMIDITY_SENSOR_ACTIVATION: 1,
    Parameter.VOLTAGE_SENSOR_ACTIVATION: 1,
    Parameter.HUMIDITY_THRESHOLD: 1,
    Parameter.CURRENT_RTC_BATTERY_VOLTAGE: 2,
    Parameter.CURRENT_HUMIDITY: 1,
    Parameter.CURRENT_VOLTAGE_SENSOR_STATE: 1,
    Parameter.CURRENT_RELAY_SENSOR_STATE: 1,
    Parameter.MANUAL_SPEED: 1,
    Parameter.FAN1RPM: 2,
    Parameter.FAN2RPM: 2,
    Parameter.FILTER_TIMER: 3,
    Parameter.RESET_FILTER_TIMER: 1,
    Parameter.BOOST_MODE_DEACTIVATION_DELAY: 1,
    Parameter.RTC_TIME: 3,
    Parameter.RTC_CALENDAR: 4,
    Parameter.WEEKLY_SCHEDULE: 1,
    Parameter.SCHEDULE_SETUP: 6,
    Parameter.SEARCH: 16,
    Parameter.MACHINE_HOURS: 4,
    Parameter.RESET_ALARMS: 1,
    Parameter.READ_ALARM: 1,
    Parameter.CLOUD_SERVER_OPERATION_PERMISSION: 1,
    Parameter.READ_FIRMWARE_VERSION: 6,
    Parameter.RESTORE_FACTORY_SETTINGS: 1,
    Parameter.FILTER_ALARM: 1,
    Parameter.WIFI_MODE: 1,
    Parameter.WIFI_NAME: 0,
    Parameter.WIFI_PASSWORD: 0,
    Parameter.WIFI_ENCRYPTION: 1,
    Parameter.WIFI_CHANNEL: 1,
    Parameter.WIFI_DHCP: 1,
    Parameter.IP_ADDRESS: 4,
    Parameter.SUBNET_MASK: 4,
    Parameter.VENTILATION_MODE: 1,
    Parameter.UNIT_TYPE: 2,
}

def get_size(parameter: Parameter) -> int:
    """
    Gets the size in bytes for a given parameter.

    :param parameter: The Parameter for which to get the size.
    :return: The size in bytes of the parameter, or -1 if the parameter is unknown.
    """
    return details.get(parameter, -1)

