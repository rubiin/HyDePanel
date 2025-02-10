from fabric.bluetooth.service import BluetoothClient, BluetoothDevice
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.scrolledwindow import ScrolledWindow

from shared.submenu import QuickSubMenu, QuickSubToggle


class BluetoothDeviceBox(CenterBox):
    """A widget to display a Bluetooth device in a box."""

    def __init__(self, device: BluetoothDevice, **kwargs):
        # TODO: FIX STYLING, make it look better
        super().__init__(
            spacing=2, style_classes="submenu-button", h_expand=True, **kwargs
        )
        self.device: BluetoothDevice = device

        self.connect_button = Button(style_classes="submenu-button")
        self.connect_button.connect(
            "clicked",
            lambda _: self.device.set_property("connecting", not self.device.connected),
        )

        self.device.connect("notify::connecting", self.on_device_connecting)
        self.device.connect("notify::connected", self.on_device_connect)

        self.add_start(
            Image(
                icon_name=device.icon_name + "-symbolic",
                icon_size=24,
                style_classes="submenu-icon",
            )
        )
        self.add_start(Label(label=device.name, style_classes="submenu-label1"))  # type: ignore
        self.add_end(self.connect_button)

        self.on_device_connect()

    def on_device_connecting(self, device, _):
        if self.device.connecting:
            self.connect_button.set_label("connecting...")
        elif self.device.connected is False:
            self.connect_button.set_label("failed to connect")

    def on_device_connect(self, *args):
        self.connect_button.set_label(
            "connected",
        ) if self.device.connected else self.connect_button.set_label("disconnected")


class BluetoothSubMenu(QuickSubMenu):
    """A submenu to display the Bluetooth settings."""

    def __init__(self, client: BluetoothClient, **kwargs):
        self.client = client
        self.client.connect("device-added", self.populate_new_device)

        self.paired_devices = Box(
            orientation="v",
            spacing=4,
            h_expand=True,
            children=Label("Paired Devices", h_align="start"),
        )

        for device in self.client.devices:
            if device.paired:
                self.paired_devices.add(BluetoothDeviceBox(device))

        self.available_devices = Box(
            orientation="v",
            spacing=4,
            h_expand=True,
            children=Label("Available Devices", h_align="start"),
        )

        self.scan_button = Button(
            image=Image(icon_name="view-refresh-symbolic", icon_size=18),
            name="submenu-button",
        )
        self.scan_button.connect("clicked", self.on_scan_toggle)

        self.child = ScrolledWindow(
            min_content_size=(-1, 100),
            max_content_size=(-1, 100),
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
            title_icon="bluetooth-active-symbolic",
            scan_button=self.scan_button,
            child=Box(
                orientation="v",
                children=[ self.child],
            ),
            **kwargs,
        )

    def on_scan_toggle(self, btn: Button):
        self.client.toggle_scan()
        btn.set_style_classes(
            ["active"]
        ) if self.client.scanning else btn.set_style_classes([""])

    def populate_new_device(self, client: BluetoothClient, address: str):
        device: BluetoothDevice = client.get_device(address)
        if device.paired:
            self.paired_devices.add(BluetoothDeviceBox(device))
        else:
            self.available_devices.add(BluetoothDeviceBox(device))


class BluetoothToggle(QuickSubToggle):
    """A widget to display the Bluetooth status."""

    def __init__(self, submenu: QuickSubMenu, client: BluetoothClient, **kwargs):
        super().__init__(
            action_label="Not Connected",
            action_icon="bluetooth-active-symbolic",
            submenu=submenu,
            **kwargs,
        )
        # Client Signals
        self.client = client
        self.client.connect("notify::enabled", self.toggle_bluetooth)
        self.client.connect("device-added", self.new_device)

        self.toggle_bluetooth(client)

        for device in self.client.devices:
            self.new_device(client, device.address)
        self.device_connected(
            self.client.connected_devices[0]
        ) if self.client.connected_devices else None

        # Button Signals
        self.connect("action-clicked", lambda *_: self.client.toggle_power())

    def toggle_bluetooth(self, client: BluetoothClient, *_):
        if client.enabled:
            self.set_active_style(True)
            self.action_icon.set_from_icon_name("bluetooth-active-symbolic", 18)
            self.action_label.set_label("Not Connected")
        else:
            self.set_active_style(False)
            self.action_icon.set_from_icon_name("bluetooth-disabled-symbolic", 18)
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
                else "Not Connected"
            )
