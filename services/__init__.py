from fabric.audio import Audio
from fabric.bluetooth import BluetoothClient

from .battery import BatteryService
from .brightness import BrightnessService
from .custom_notification import CustomNotifications
from .mpris import MprisPlayer, MprisPlayerManager
from .network import NetworkService, Wifi
from .networkspeed import NetworkSpeed
from .power_profile import PowerProfilesService
from .screen_record import ScreenRecorderService
from .weather import WeatherService

# Fabric services
audio_service = Audio()
notification_service = CustomNotifications()
bluetooth_service = BluetoothClient()


__all__ = [
    "BatteryService",
    "BrightnessService",
    "CustomNotifications",
    "MprisPlayer",
    "MprisPlayerManager",
    "NetworkService",
    "NetworkSpeed",
    "PowerProfilesService",
    "ScreenRecorderService",
    "WeatherService",
    "Wifi",
    "audio_service",
    "bluetooth_service",
    "notification_service",
]
