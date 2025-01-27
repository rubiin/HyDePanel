import gi
from fabric.bluetooth import BluetoothClient
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from gi.repository import Gtk

import utils.icons as icons
from shared.pop_over import PopOverWindow
from shared.widget_container import ButtonWidget
from utils.widget_settings import BarConfig

gi.require_version("Gtk", "3.0")

class BlueToothMenu(Box):
    """A menu to display the Bluetooth devices."""

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            name="bluetooth-box",
            pass_through=True,
            **kwargs,
        )

        self.header = Box(
            name="bluetooth-header",
            orientation="h",
            spacing=10,
            children=[
                Label(
                    label="Bluetooth",
                    style_classes="panel-text",
                ),
            ],
        )
        self.header.pack_end(
            Box(
                spacing=10,
                children=(
                    Gtk.Switch(
                        name="notification-switch",
                        active=False,
                        valign=Gtk.Align.CENTER,
                        visible=True,
                    ),
                    Button(
                        image=Image(
                            icon_name="view-refresh-symbolic",
                            icon_size=16
                        )
                    ),
                )
            ),
            False,
            False,
            0,
        )

        self.children = self.header


class BlueToothWidget(ButtonWidget):
    """A widget to display the Bluetooth status."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(**kwargs)
        self.bluetooth_client = BluetoothClient()

        self.box = Box()

        self.children = self.box

        self.icons = icons.icons["bluetooth"]

        self.config = widget_config["bluetooth"]

        self.bluetooth_icon = Image(
            icon_name=self.icons["enabled"],
            icon_size=self.config["icon_size"],
        )

        self.bt_label = Label(label="", visible=False, style_classes="panel-text")

        self.bluetooth_client.connect("changed", self.update_bluetooth_status)

        popup = PopOverWindow(
            parent=bar,
            name="bluetooth-menu-popover",
            child=BlueToothMenu(),
            visible=False,
            all_visible=False,
        )

        self.connect(
            "clicked",
            lambda *_: popup.set_visible(not popup.get_visible()),
        )

        popup.set_pointing_to(self)

        self.update_bluetooth_status()

    def update_bluetooth_status(self, *args):
        bt_status = "on" if self.bluetooth_client.enabled else "off"

        icon = self.icons["enabled"] if bt_status == "on" else self.icons["disabled"]

        self.bluetooth_icon.set_from_icon_name(icon, icon_size=self.config["icon_size"])
        self.box.children = (self.bluetooth_icon, self.bt_label)

        if self.config["label"]:
            self.bt_label.set_text(bt_status.capitalize())
            self.bt_label.show()

        if self.config["tooltip"]:
            self.set_tooltip_text(f"Bluetooth is {bt_status}")

    def on_destroy(self):
        self.bluetooth_client.disconnect("changed", self.update_bluetooth_status)
