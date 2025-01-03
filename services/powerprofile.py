import dbus
from dbus.mainloop.glib import DBusGMainLoop
from fabric import Service
from loguru import logger


class PowerProfiles(Service):
    """Service to interact with the PowerProfiles service."""

    instance = None

    @staticmethod
    def get_initial():
        if PowerProfiles.instance is None:
            PowerProfiles.instance = PowerProfiles()

        return PowerProfiles.instance

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            **kwargs,
        )

        self.bus_name = "net.hadess.PowerProfiles"
        self.object_path = "/net/hadess/PowerProfiles"

        self.power_profiles = {
            "performance": {
                "name": "Performance",
                "icon_name": "power-profile-performance-symbolic",
            },
            "balanced": {
                "name": "Balanced",
                "icon_name": "power-profile-balanced-symbolic",
            },
            "power-saver": {
                "name": "Power Saver",
                "icon_name": "power-profile-power-saver-symbolic",
            },
        }

        # Set up the dbus main loop
        DBusGMainLoop(set_as_default=True)

        self.bus = dbus.SystemBus()

        self.power_profiles = self.bus.get_object(self.bus_name, self.object_path)

        self.iface = dbus.Interface(
            self.power_profiles, "org.freedesktop.DBus.Properties"
        )

        # Connect the 'g-properties-changed' signal to the handler
        self.iface.connect_to_signal("PropertiesChanged", self.handle_property_change)

    def get_current_profile(self):
        try:
            profile = self.iface.Get("net.hadess.PowerProfiles", "ActiveProfile")
            return self.power_profiles.get(profile, self.power_profiles["balanced"])
        except dbus.DBusException as e:
            logger.error(f"[PowerProfile] Error retrieving current power profile: {e}")
            return self.power_profiles["balanced"]

    def set_power_profile(self, profile):
        try:
            self.iface.Set(self.bus_name, "ActiveProfile", dbus.String(profile))
            logger.info(f"[PowerProfile] Power profile set to {profile}")
        except dbus.DBusException as e:
            logger.error(
                f"[PowerProfile] Could not change power level to {profile}: {e}"
            )

    # Function to handle properties change signals
    def handle_property_change(self, proxy, changed, invalidated):
        # Print the changed ActiveProfile
        if "ActiveProfile" in changed:
            print("ActiveProfile changed:", changed["ActiveProfile"])
