from gi.repository import Gio, GLib


class GioDBusHelper:
    """A helper class for interacting with D-Bus using the Gio library."""

    """A helper class for interacting with D-Bus using the Gio library."""

    def __init__(
        self,
        bus_name,
        object_path,
        interface_name,
        bus_type=Gio.BusType.SYSTEM,
    ):
        self.bus = Gio.bus_get_sync(bus_type, None)
        self.proxy = Gio.DBusProxy.new_sync(
            self.bus,
            Gio.DBusProxyFlags.NONE,
            None,
            bus_name,
            object_path,
            interface_name,
            None,
        )

    def call_method(
        self,
        bus_name,
        object_path,
        interface_name,
        method_name,
        parameters=None,
        timeout=-1,
    ):
        if parameters is None:
            parameters = GLib.Variant("()", ())
        result = self.bus.call_sync(
            bus_name,
            object_path,
            interface_name,
            method_name,
            parameters,
            None,
            Gio.DBusCallFlags.NONE,
            timeout,
            None,
        )
        return result.unpack()

    def listen_signal(self, sender, interface_name, member, object_path, callback):
        """Register a signal listener (conn, sender, path, iface, signal, parameters)"""
        self.bus.signal_subscribe(
            sender,
            interface_name,
            member,
            object_path,
            arg0=None,
            flags=Gio.DBusSignalFlags.NONE,
            callback=callback,
        )

    def set_property(
        self, bus_name, object_path, interface_name, property_name, value_variant
    ):
        """Sets a D-Bus property using the standard D-Bus Properties interface."""
        return self.call_method(
            bus_name=bus_name,
            object_path=object_path,
            interface_name="org.freedesktop.DBus.Properties",
            method_name="Set",
            parameters=GLib.Variant(
                "(ssv)", (interface_name, property_name, value_variant)
            ),
        )
