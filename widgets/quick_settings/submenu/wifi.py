from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.scrolledwindow import ScrolledWindow

from services import NetworkService, Wifi
from shared import HoverButton, QSChevronButton, QuickSubMenu, ScanButton
from utils import symbolic_icons


class WifiSubMenu(QuickSubMenu):
    """A submenu to display the Wifi settings."""

    def __init__(self, **kwargs):
        self.client = NetworkService()

        self.client.connect("device-ready", self.on_device_ready)

        self.available_networks_box = Box(orientation="v", spacing=4, h_expand=True)

        self.scan_button = ScanButton()

        self.scan_button.set_sensitive(False)

        self.scan_button.connect("clicked", self.start_new_scan)

        self.child = ScrolledWindow(
            min_content_size=(-1, 190),
            max_content_size=(-1, 190),
            propagate_width=True,
            propagate_height=True,
            child=self.available_networks_box,
        )

        super().__init__(
            title="Network",
            title_icon=symbolic_icons["network"]["wifi"]["generic"],
            scan_button=self.scan_button,
            child=self.child,
            **kwargs,
        )

    def on_scan(self, _, value, *args):
        """Called when the scan is complete."""

        if value:
            self.scan_button.play_animation()
        else:
            self.scan_button.stop_animation()

    def start_new_scan(self, *_):
        self.wifi_device.scan()
        self.build_wifi_options()
        self.scan_button.play_animation()

    def on_device_ready(self, client: NetworkService):
        self.wifi_device = client.wifi_device
        if self.wifi_device:
            self.scan_button.set_sensitive(True)
            self.start_new_scan(None)
            self.wifi_device.connect("changed", self.start_new_scan)

    def build_wifi_options(self):
        self.available_networks_box.children = []
        for ap in self.wifi_device.access_points:
            if ap.get("ssid") != "Unknown":
                btn = self.make_button_from_ap(ap)
                self.available_networks_box.add(btn)

    def make_button_from_ap(self, ap) -> Button:
        security_label = ""

        ap_container = Box(
            style="padding: 5px;",
            orientation="h",
            spacing=4,
            tooltip_markup=ap.get("ssid"),
            children=[
                Image(
                    icon_name=ap.get("icon-name"),
                    icon_size=18,
                ),
                Label(
                    label=ap.get("ssid"),
                    style_classes="submenu-item-label",
                    ellipsization="end",
                    v_align="center",
                    h_align="start",
                    h_expand=True,
                ),
            ],
        )

        ap_button = HoverButton(style_classes="submenu-button", name="wifi-ap-button")

        if self.wifi_device.state == "activated" and self.wifi_device.is_active_ap(
            ap.get("ssid")
        ):
            security_label = " " + security_label

            if self.wifi_device.get_ap_security(ap.get("active-ap")) != "unsecured":
                security_label = security_label + ""

        ap_container.add(
            Label(
                markup=f"<b>{security_label}</b>",
                style="font-size: 14px",
                v_align="center",
            )
        )

        ap_button.add(ap_container)

        ap_button.connect(
            "clicked", lambda *_: self.wifi_device.disconnect_network(ap.get("ssid"))
        )
        return ap_button


class WifiToggle(QSChevronButton):
    """A widget to display a toggle button for Wifi."""

    def __init__(self, submenu: QuickSubMenu, **kwargs):
        super().__init__(
            action_icon=symbolic_icons["network"]["wifi"]["generic"],
            action_label=" Wifi Disabled",
            submenu=submenu,
            **kwargs,
        )
        self.client = NetworkService()
        self.client.connect("device-ready", self.update_action_button)

        self.connect("action-clicked", self.on_action)

    def update_action_button(self, client: NetworkService):
        wifi = client.wifi_device

        if wifi:
            wifi.connect(
                "notify::enabled",
                lambda *_: self.set_active_style(wifi.get_property("enabled")),  # type: ignore
            )
            wifi.connect("changed", self.update_status)

            self.action_icon.set_from_icon_name(
                wifi.get_property("icon-name") + "-symbolic", self.pixel_size
            )
            wifi.bind_property("icon-name", self.action_icon, "icon-name")

            self.action_label.set_label(wifi.get_property("ssid"))
            wifi.bind_property("ssid", self.action_label, "label")

        else:
            self.action_button.set_sensitive(False)
            self.action_label.set_label("Wi-Fi device not available.")

    def on_action(self, btn):
        wifi: Wifi | None = self.client.wifi_device
        if wifi:
            wifi.toggle_wifi()

    def update_status(self, wifi: Wifi):
        self.action_icon.set_from_icon_name(
            wifi.icon_name,
            self.pixel_size,
        )
