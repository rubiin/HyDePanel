import gi
from fabric.widgets.box import Box
from fabric.widgets.label import Label

gi.require_version("Gst", "1.0")
from gi.repository import Gst, Gtk


class LofiMenu(Box):
    "A menu for playing online radio stations using GStreamer."

    def __init__(self):
        super().__init__()

        # Initialize GStreamer
        Gst.init(None)

        # List of radio stations: (Name, URL)
        self.stations = [
            ("NPR", "https://npr-ice.streamguys1.com/live.mp3"),
            (
                "BBC World Service",
                "http://bbcwssc.ic.llnwd.net/stream/bbcwssc_mp1_ws-eieuk",
            ),
            ("Radio Paradise", "http://stream.radioparadise.com/aac-320"),
        ]

        # Listbox to show stations
        self.listbox = Gtk.ListBox(visible=True)
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.listbox.connect("row-selected", self.on_station_selected)

        # Add stations to listbox
        for name, url in self.stations:
            label = Label(label=name, h_align="center", v_align="center")
            row = Gtk.ListBoxRow(visible=True, name="station_row")
            row.add(label)
            row.station_url = url
            row.station_name = name
            self.listbox.add(row)

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
