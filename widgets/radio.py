from typing import ClassVar

import gi
from fabric.utils import cooldown
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.scrolledwindow import ScrolledWindow
from gi.repository import GObject, Gst, Gtk

from shared.pop_over import Popover
from shared.widget_container import ButtonWidget
from utils.widget_settings import BarConfig
from utils.widget_utils import text_icon

gi.require_version("Gst", "1.0")


class RadioMenu(Box):
    "A menu for playing online radio stations using GStreamer."

    __gsignals__: ClassVar = {"changed": (GObject.SignalFlags.RUN_FIRST, None, (str,))}

    def __init__(self, config, **kwargs):
        super().__init__(name="radio_menu", **kwargs)

        # Initialize GStreamer
        Gst.init(None)

        row_height_px = 40  # Height of each row in pixels

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
            {
                "name": "Radio - Chillhop de 🎧🎶",
                "url": "https://streams.fluxfm.de/Chillhop/mp3-128/streams.fluxfm.de/",
            },
            {
                "name": "Radion - NeoLofi 🎧🎶",
                "url": "https://streams.fluxfm.de/neofm/mp3-320/radiode/",
            },
            {
                "name": "Radio - XJazz 🎧🎶",
                "url": "https://streams.fluxfm.de/xjazz/mp3-320/audio/",
            },
        ]

        # Listbox to show stations
        self.listbox = Gtk.ListBox(visible=True)
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.listbox.connect("row-activated", self.on_station_selected)

        self.scrolled_window = ScrolledWindow(
            name="radio_scrolled_window",
            v_scrollbar_policy="automatic",
            h_scrollbar_policy="never",
            size=(300, config["max_visible_stations"] * row_height_px),
            child=self.listbox,
        )

        # Add stations to listbox
        for station in self.stations:
            name = station["name"]
            url = station["url"]
            label = Label(
                label=name, name="station_label", v_align="center", h_align="start"
            )
            row = Gtk.ListBoxRow(visible=True, name="station_row")
            row.add(label)
            row.station_url = url
            row.station_name = name
            self.listbox.add(row)

        self.add(self.scrolled_window)

        # GStreamer player
        self.player = Gst.ElementFactory.make("playbin", "player")
        self.current_row = None

    def on_station_selected(self, _, row):
        if row is not None:
            url = row.station_url
            name = row.station_name

            # Stop previous stream
            self.player.set_state(Gst.State.NULL)

            # Play new stream
            self.player.set_property("uri", url)
            self.player.set_state(Gst.State.PLAYING)

            # Remove style from previous row
            if self.current_row:
                self.current_row.get_style_context().remove_class("playing")

            # Add style to current row
            row.get_style_context().add_class("playing")
            self.current_row = row
            self.emit("changed", name)

    @cooldown(1)
    def cycle_stations(self):
        """Cycle through the stations."""
        if not self.stations:
            return

        if self.current_row is None:
            self.current_row = self.listbox.get_row_at_index(0)
        else:
            next_index = (self.listbox.get_row_index(self.current_row) + 1) % len(
                self.stations
            )
            self.current_row = self.listbox.get_row_at_index(next_index)

        self.on_station_selected(None, self.current_row)


class RadioWidget(ButtonWidget):
    """a widget that displays the title of the active window."""

    def __init__(self, widget_config: BarConfig, **kwargs):
        super().__init__(widget_config["radio_player"], name="radio_player", **kwargs)

        # Create a TextIcon with the specified icon and size
        self.icon = text_icon(
            icon=self.config["icon"],
            props={"style_classes": "panel-font-icon"},
        )
        self.box.add(self.icon)

        # Create a label to display the current station
        if self.config["label"]:
            self.label = Label(
                label="No station playing",
                style_classes="panel-text",
                name="lofi_label",
            )
            self.box.add(self.label)

        radio_menu = RadioMenu(config=self.config)

        self.popover = Popover(
            content_factory=lambda: radio_menu,
            point_to=self,
        )
        self.connect("clicked", self.popover.open)

        radio_menu.connect("changed", self.handle_station_change)

    def handle_station_change(self, _, name):
        """Handle play button click."""

        if self.config["label"]:
            # Update the label with the name of the currently playing station
            self.label.set_label(f"Now playing: {name}")

        if self.config["tooltip"]:
            # Update the tooltip with the name of the currently playing station
            self.set_tooltip_text(f"Now playing: {name}")
