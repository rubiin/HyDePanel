from typing import ClassVar
import gi
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from gi.repository import Gst, Gtk, GObject

from shared.pop_over import Popover
from shared.widget_container import ButtonWidget
from utils.widget_settings import BarConfig
from utils.widget_utils import text_icon

gi.require_version("Gst", "1.0")


class LofiMenu(Box):
    "A menu for playing online radio stations using GStreamer."

    __gsignals__: ClassVar = {
        "changed": (GObject.SignalFlags.RUN_FIRST, None, (int,))
    }

    def __init__(self):
        super().__init__(name="lofi_menu")

        # Initialize GStreamer
        Gst.init(None)

        # List of radio stations: (Name, URL)
        self.stations = [
            {
                "name": "Radio - Lofi Girl 🎧🎶",
                "url": "https://play.streamafrica.net/lofiradio",
            },
            {
                "name": "Radio - Chillhop 🎧🎶",
                "url": "http://stream.zeno.fm/fyn8eh3h5f8uv",
            },
        ]

        # Listbox to show stations
        self.listbox = Gtk.ListBox(visible=True)
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.listbox.connect("row-activated", self.on_station_selected)

        # Add stations to listbox
        for station in self.stations:
            name = station["name"]
            url = station["url"]
            label = Label(label=name, name="station_label", v_align="center")
            row = Gtk.ListBoxRow(visible=True, name="station_row")
            row.add(label)
            row.station_url = url
            row.station_name = name
            self.listbox.add(row)

        self.add(self.listbox)

        # GStreamer player
        self.player = Gst.ElementFactory.make("playbin", "player")
        self.current_row = None

    def on_station_selected(self, _, row):
        if row is not None:
            url = row.station_url

            # Stop previous stream
            self.player.set_state(Gst.State.NULL)

            # Play new stream
            self.player.set_property("uri", url)
            self.player.set_state(Gst.State.PLAYING)

            # Remove style from previous row
            if self.current_row:
                self.current_row.remove_class("playing")

            # Add style to current row
            row.add_class("playing")
            self.current_row = row
            self.emit("changed", row)


class LofiWidget(ButtonWidget):
    """a widget that displays the title of the active window."""

    def __init__(self, widget_config: BarConfig, **kwargs):
        super().__init__(widget_config["lofi_player"], name="lofi_player", **kwargs)

        # Create a TextIcon with the specified icon and size
        self.icon = text_icon(
            icon=self.config["icon"],
            props={"style_classes": "panel-font-icon"},
        )
        self.box.add(self.icon)

        self.box.set_spacing(10)

        if self.config["label"]:
            self.box.add(Label(label="lofi_player", style_classes="panel-text"))

        lofi_menu = LofiMenu()

        self.popover = Popover(
            content_factory=lambda: lofi_menu,
            point_to=self,
        )
        self.connect("clicked", self.popover.open)

        lofi_menu.connect("changed", lambda _, row: print(f"Selected station: {row.station_name}"))
