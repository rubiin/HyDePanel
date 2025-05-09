from fabric.bluetooth.service import BluetoothClient, BluetoothDevice
from fabric.utils import bulk_connect
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.scrolledwindow import ScrolledWindow

from services import bluetooth_service
from shared import HoverButton, QSChevronButton, QuickSubMenu
from shared.submenu import ScanButton
from utils.icons import icons


class BluetoothDeviceBox(CenterBox):
    """A widget to display a Bluetooth device in a box."""

    def __init__(self, device: BluetoothDevice, **kwargs):
        super().__init__(
            spacing=2,
            style_classes="submenu-button",
            h_expand=True,
            name="bluetooth-device-box",
            **kwargs,
        )
        self.device: BluetoothDevice = device

        self.connect_button = HoverButton(style_classes="submenu-button")
        self.connect_button.connect(
            "clicked",
            lambda _: self.device.set_property("connecting", not self.device.connected),
        )

        bulk_connect(
            self.device,
            {
                "notify::connecting": self.on_device_connecting,
                "notify::connected": self.on_device_connect,
            },
        )

        self.add_start(
            Image(
                icon_name=device.icon_name + "-symbolic",
                icon_size=18,
            )
        )
        self.add_start(
            Label(
                label=device.name,
                style_classes="submenu-item-label",
                ellipsization="end",
            )
        )  # type: ignore
        self.add_end(self.connect_button)

        self.on_device_connect()

    def on_device_connecting(self, device, _):
        if self.device.connecting:
            self.connect_button.set_label("Connecting...")
        elif self.device.connected is False:
            self.connect_button.set_label("Failed to connect")

    def on_device_connect(self, *args):
        self.connect_button.set_label(
            "Disconnect",
        ) if self.device.connected else self.connect_button.set_label("Connect")


class BluetoothSubMenu(QuickSubMenu):
    """A submenu to display the Bluetooth settings."""

    def __init__(self, **kwargs):
        self.client = bluetooth_service
        self.client.connect("device-added", self.populate_new_device)

        self.paired_devices = Box(
            orientation="v",
            spacing=10,
            h_expand=True,
            children=Label(
                "Paired Devices",
                h_align="start",
                style_classes="panel-text",
            ),
        )

        for device in self.client.devices:
            if device.paired:
                self.paired_devices.add(BluetoothDeviceBox(device))

        self.available_devices = Box(
            orientation="v",
            spacing=4,
            h_expand=True,
            children=Label(
                "Available Devices",
                h_align="start",
                style="margin:12px 0;",
                style_classes="panel-text",
            ),
        )

        self.scan_button = ScanButton()
        self.scan_button.connect("clicked", self.on_scan_toggle)

        self.child = ScrolledWindow(
            min_content_size=(-1, 190),
            max_content_size=(-1, 190),
            propagate_width=True,
            propagate_height=True,
            child=Box(
                orientation="v",
                children=Box(
                    orientation="v",
                    children=[self.paired_devices, self.available_devices],
                ),
            ),
        )

        super().__init__(
            title="Bluetooth",
            title_icon=icons["bluetooth"]["enabled"],
            scan_button=self.scan_button,
            child=Box(
                orientation="v",
                children=[self.child],
            ),
            **kwargs,
        )

    def on_scan_toggle(self, btn: Button):
        self.client.toggle_scan()
        btn.set_style_classes(
            ["active"]
        ) if self.client.scanning else btn.set_style_classes([""])

        if self.client.scanning:
            self.scan_button.play_animation()
        else:
            self.scan_button.stop_animation()

    def populate_new_device(self, client: BluetoothClient, address: str):
        device: BluetoothDevice = client.get_device(address)
        if device.paired:
            self.paired_devices.add(BluetoothDeviceBox(device))
        else:
            self.available_devices.add(BluetoothDeviceBox(device))


class BluetoothToggle(QSChevronButton):
    """A widget to display the Bluetooth status."""

    def __init__(self, submenu: QuickSubMenu, **kwargs):
        super().__init__(
            action_label="Enabled",
            action_icon=icons["bluetooth"]["enabled"],
            submenu=submenu,
            **kwargs,
        )

        # Client Signals
        self.client = bluetooth_service

        bulk_connect(
            self.client,
            {"device-added": self.new_device, "notify::enabled": self.toggle_bluetooth},
        )

        self.toggle_bluetooth(self.client)

        for device in self.client.devices:
            self.new_device(self.client, device.address)
        self.device_connected(
            self.client.connected_devices[0]
        ) if self.client.connected_devices else None

        # Button Signals
        self.connect("action-clicked", lambda *_: self.client.toggle_power())

    def toggle_bluetooth(self, client: BluetoothClient, *_):
        if client.enabled:
            self.set_active_style(True)
            self.action_icon.set_from_icon_name(icons["bluetooth"]["enabled"], 18)
            self.action_label.set_label("Enabled")
        else:
            self.set_active_style(False)
            self.action_icon.set_from_icon_name(icons["bluetooth"]["disabled"], 18)
            self.action_label.set_label("Disabled")

    def new_device(self, client: BluetoothClient, address):
        device: BluetoothDevice = client.get_device(address)
        device.connect("changed", self.device_connected)

    def device_connected(self, device: BluetoothDevice):
        if device.connected:
            self.action_label.set_label(device.name)
        elif self.action_label.get_label() == device.name:
            self.action_label.set_label(
                self.client.connected_devices[0].name
                if self.client.connected_devices
                else "Enabled"
            )
