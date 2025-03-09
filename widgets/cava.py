import configparser
import ctypes
import os
import signal
import struct
import subprocess
import threading
from math import pi

from fabric.utils import get_relative_path
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay
from fabric.widgets.stack import Stack
from gi.repository import Gdk, GLib, Gtk
from loguru import logger

from services.mpris import MprisPlayer, MprisPlayerManager
from shared import HoverButton
from utils.icons import common_text_icons
from utils.widget_settings import BarConfig


def get_bars(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return int(config["general"]["bars"])


CAVA_CONFIG = get_relative_path("../assets/cava.ini")

bars = get_bars(CAVA_CONFIG)


def get_player_icon_markup_by_name(player_name):
    if player_name:
        pn = player_name.lower()
        if pn == "firefox" or pn == "plasma-browser-integration":
            return common_text_icons["firefox"]
        elif pn == "spotify":
            return common_text_icons["spotify"]
        elif pn in ("chromium", "brave"):
            return common_text_icons["chromium"]
    return common_text_icons["disc"]


def set_death_signal():
    """
    Set the death signal of the child process to SIGTERM so that if the parent
    process is killed, the child (cava) is automatically terminated.
    """
    libc = ctypes.CDLL("libc.so.6")
    PR_SET_PDEATHSIG = 1
    libc.prctl(PR_SET_PDEATHSIG, signal.SIGTERM)


class Cava:
    """
    CAVA wrapper.
    Launch cava process with certain settings and read output.
    """

    NONE = 0
    RUNNING = 1
    RESTARTING = 2
    CLOSING = 3

    def __init__(self, mainapp):
        self.bars = bars
        self.path = "/tmp/cava.fifo"

        self.cava_config_file = CAVA_CONFIG
        self.data_handler = mainapp.draw.update
        self.command = ["cava", "-p", self.cava_config_file]
        self.state = self.NONE

        self.env = dict(os.environ)
        self.env["LC_ALL"] = "en_US.UTF-8"  # not sure if it's necessary

        is_16bit = True
        self.byte_type, self.byte_size, self.byte_norm = (
            ("H", 2, 65535) if is_16bit else ("B", 1, 255)
        )

        if not os.path.exists(self.path):
            os.mkfifo(self.path)

    def _run_process(self):
        logger.debug("Launching cava process...")
        try:
            self.process = subprocess.Popen(
                self.command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=self.env,
                preexec_fn=set_death_signal,  # Ensure cava gets killed when the parent dies.
            )
            logger.debug("cava successfully launched!")
            self.state = self.RUNNING
        except Exception:
            logger.exception("Fail to launch cava")

    def _start_reader_thread(self):
        logger.debug("Activate cava stream handler")
        self.thread = threading.Thread(target=self._read_output)
        self.thread.daemon = True
        self.thread.start()

    def _read_output(self):
        fifo = open(self.path, "rb")
        chunk = self.byte_size * self.bars  # number of bytes for given format
        fmt = self.byte_type * self.bars  # pack of given format
        while True:
            data = fifo.read(chunk)
            if len(data) < chunk:
                break
            sample = [i / self.byte_norm for i in struct.unpack(fmt, data)]
            GLib.idle_add(self.data_handler, sample)
        fifo.close()
        GLib.idle_add(self._on_stop)

    def _on_stop(self):
        logger.debug("Cava stream handler deactivated")
        if self.state == self.RESTARTING:
            if not self.thread.isAlive():
                self.start()
            else:
                logger.error("Can't restart cava, old handler still alive")
        elif self.state == self.RUNNING:
            self.state = self.NONE
            logger.error("Cava process was unexpectedly terminated.")
            # self.restart()  # May cause infinity loop, need more check

    def start(self):
        """Launch cava"""
        self._start_reader_thread()
        self._run_process()

    def restart(self):
        """Restart cava process"""
        if self.state == self.RUNNING:
            logger.debug("Restarting cava process (normal mode) ...")
            self.state = self.RESTARTING
            if self.process.poll() is None:
                self.process.kill()
        elif self.state == self.NONE:
            logger.warning("Restarting cava process (after crash) ...")
            self.start()

    def close(self):
        """Stop cava process"""
        self.state = self.CLOSING
        if self.process.poll() is None:
            self.process.kill()
        os.remove(self.path)


class AttributeDict(dict):
    """Dictionary with keys as attributes. Does nothing but easy reading"""

    def __getattr__(self, attr):
        return self.get(attr, 3)

    def __setattr__(self, attr, value):
        self[attr] = value


class Spectrum:
    """Spectrum drawing"""

    def __init__(self):
        self.silence_value = 0
        self.audio_sample = []
        self.color = None

        self.area = Gtk.DrawingArea()
        self.area.connect("draw", self.redraw)
        self.area.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)

        self.sizes = AttributeDict()
        self.sizes.area = AttributeDict()
        self.sizes.bar = AttributeDict()

        self.silence = 10
        self.max_height = 12

        self.area.connect("configure-event", self.size_update)
        self.color_update()

    def is_silence(self, value):
        """Check if volume level critically low during last iterations"""
        self.silence_value = 0 if value > 0 else self.silence_value + 1
        return self.silence_value > self.silence

    def update(self, data):
        """Audio data processing"""
        self.color_update()
        self.audio_sample = data
        if not self.is_silence(self.audio_sample[0]):
            self.area.queue_draw()
        elif self.silence_value == (self.silence + 1):
            self.audio_sample = [0] * self.sizes.number
            self.area.queue_draw()

    # noinspection PyUnusedLocal
    def redraw(self, widget, cr):
        """Draw spectrum graph"""
        cr.set_source_rgba(*self.color)

        dx = 3

        center_y = self.sizes.area.height / 2
        for i, value in enumerate(self.audio_sample):
            width = self.sizes.area.width / self.sizes.number - self.sizes.padding
            radius = width / 2
            height = max(self.sizes.bar.height * min(value, 1), self.sizes.zero) / 2
            if height == self.sizes.zero / 2 + 1:
                height *= 0.5

            height = min(height, self.max_height)

            cr.rectangle(dx, center_y - height, width, height * 2)
            cr.arc(dx + radius, center_y - height, radius, 0, 2 * pi)
            cr.arc(dx + radius, center_y + height, radius, 0, 2 * pi)

            cr.close_path()
            # cr.rectangle(0, center_y, self.sizes.area.width, 20)

            dx += width + self.sizes.padding
        cr.fill()

    # noinspection PyUnusedLocal
    def size_update(self, *args):
        """Update drawing geometry"""
        self.sizes.number = bars
        self.sizes.padding = 100 / bars
        self.sizes.zero = 0

        self.sizes.area.width = self.area.get_allocated_width()
        self.sizes.area.height = self.area.get_allocated_height() - 2

        tw = self.sizes.area.width - self.sizes.padding * (self.sizes.number - 1)
        self.sizes.bar.width = max(int(tw / self.sizes.number), 1)
        self.sizes.bar.height = self.sizes.area.height

    def color_update(self):
        """Set drawing color according current settings by reading primary color from CSS"""
        color = "#a5c8ff"  # default value
        red = int(color[1:3], 16) / 255
        green = int(color[3:5], 16) / 255
        blue = int(color[5:7], 16) / 255
        self.color = Gdk.RGBA(red=red, green=green, blue=blue, alpha=1.0)


class SpectrumRender:
    """Spectrum widget"""

    def __init__(self, mode=None, **kwargs):
        super().__init__(**kwargs)
        self.mode = mode

        self.draw = Spectrum()
        self.cava = Cava(self)
        self.cava.start()

    def get_spectrum_box(self):
        # Get the spectrum box
        box = Overlay(name="cavalcade", h_align="center", v_align="center")
        box.set_size_request(180, 40)
        box.add_overlay(self.draw.area)
        return box


class PlayerSmall(CenterBox):
    """Compact MPRIS player widget"""

    def __init__(self, bar_config: BarConfig, bar):
        super().__init__(
            name="player-small", orientation="h", h_align="fill", v_align="center"
        )
        self._show_artist = False  # toggle flag
        self._display_options = ["cavalcade", "title", "artist"]
        self._display_index = 0
        self._current_display = "cavalcade"

        self.mpris_icon = HoverButton(
            name="compact-mpris-icon",
            h_align="center",
            v_align="center",
            child=Label(
                name="compact-mpris-icon-label", markup=common_text_icons["disc"]
            ),
        )
        # Remove scroll events; instead, add button press events.
        self.mpris_icon.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.mpris_icon.connect("button-press-event", self._on_icon_button_press)
        # Prevent the child from propagating events.
        child = self.mpris_icon.get_child()
        child.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        child.connect("button-press-event", lambda widget, event: True)

        self.mpris_label = Label(
            name="compact-mpris-label",
            label="Nothing Playing",
            ellipsization="end",
            max_chars_width=26,
            h_align="center",
        )
        self.mpris_button = HoverButton(
            name="compact-mpris-button",
            h_align="center",
            v_align="center",
            child=Label(
                name="compact-mpris-button-label", markup=common_text_icons["play"]
            ),
        )
        self.mpris_button.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.mpris_button.connect(
            "button-press-event", self._on_play_pause_button_press
        )

        self.cavalcade = SpectrumRender()
        self.cavalcade_box = self.cavalcade.get_spectrum_box()

        self.center_stack = Stack(
            name="compact-mpris",
            transition_type="crossfade",
            transition_duration=100,
            v_align="center",
            v_expand=False,
            children=[
                self.cavalcade_box,
                self.mpris_label,
            ],
        )
        self.center_stack.set_visible_child(self.cavalcade_box)  # default to cavalcade

        # Create additional compact view.
        self.mpris_small = CenterBox(
            name="compact-mpris",
            orientation="h",
            h_expand=True,
            h_align="fill",
            v_align="center",
            v_expand=False,
            start_children=self.mpris_icon,
            center_children=self.center_stack,  # Changed to center_stack to handle stack switching
            end_children=self.mpris_button,
        )

        self.add(self.mpris_small)

        self.mpris_manager = MprisPlayerManager()
        self.mpris_player = None
        self.current_index = 0

        players = self.mpris_manager.players
        if players:
            mp = MprisPlayer(players[self.current_index])
            self.mpris_player = mp
            self._apply_mpris_properties()
            self.mpris_player.connect("changed", self._on_mpris_changed)
        else:
            self._apply_mpris_properties()

        self.mpris_manager.connect("player-appeared", self.on_player_appeared)
        self.mpris_manager.connect("player-vanished", self.on_player_vanished)
        self.mpris_button.connect("clicked", self._on_play_pause_clicked)

    def _apply_mpris_properties(self):
        if not self.mpris_player:
            self.mpris_label.set_text("Nothing Playing")
            self.mpris_button.get_child().set_markup()
            self.mpris_icon.get_child().set_markup(common_text_icons["disc"])
            if self._current_display != "cavalcade":
                self.center_stack.set_visible_child(
                    self.mpris_label
                )  # if was title or artist, keep showing label
            else:
                self.center_stack.set_visible_child(
                    self.cavalcade_box
                )  # default to cavalcade if no player
            return

        mp = self.mpris_player

        # Toggle between title and artist.
        text = (
            mp.artist
            if self._show_artist and mp.artist
            else (mp.title if mp.title and mp.title.strip() else "Nothing Playing")
        )

        if len(text) > 25:
            text = text[:25] + "..."

        self.mpris_label.set_text(text)

        # Choose icon based on player name.
        player_name = (
            mp.player_name.lower()
            if hasattr(mp, "player_name") and mp.player_name
            else ""
        )
        icon_markup = get_player_icon_markup_by_name(player_name)
        self.mpris_icon.get_child().set_markup(icon_markup)
        self.update_play_pause_icon()

        if self._current_display == "title":
            text = mp.title if mp.title and mp.title.strip() else "Nothing Playing"
            self.mpris_label.set_text(text)
            self.center_stack.set_visible_child(self.mpris_label)
        elif self._current_display == "artist":
            text = mp.artist if mp.artist else "Nothing Playing"
            self.mpris_label.set_text(text)
            self.center_stack.set_visible_child(self.mpris_label)
        else:  # default cavalcade
            self.center_stack.set_visible_child(self.cavalcade_box)

    def _on_icon_button_press(self, widget, event):
        from gi.repository import Gdk

        if event.type == Gdk.EventType.BUTTON_PRESS:
            players = self.mpris_manager.players
            if not players:
                return True

            if event.button == 2:  # Middle-click: cycle display
                self._display_index = (self._display_index + 1) % len(
                    self._display_options
                )
                self._current_display = self._display_options[self._display_index]
                self._apply_mpris_properties()  # Re-apply to update label/cavalcade
                return True

            if event.button == 1:  # Left-click: next player
                self.current_index = (self.current_index + 1) % len(players)
            elif event.button == 3:  # Right-click: previous player
                self.current_index = (self.current_index - 1) % len(players)
                if self.current_index < 0:
                    self.current_index = len(players) - 1

            mp_new = MprisPlayer(players[self.current_index])
            self.mpris_player = mp_new
            # Conectar el evento "changed" para que se actualice
            self.mpris_player.connect("changed", self._on_mpris_changed)
            self._apply_mpris_properties()
            return True  # Se consume el evento
        return True

    def _on_play_pause_button_press(self, widget, event):
        if event.type == Gdk.EventType.BUTTON_PRESS:
            if event.button == 1:  # Click izquierdo -> track anterior
                if self.mpris_player:
                    self.mpris_player.play_pause()
                    self.update_play_pause_icon()
            elif event.button == 3:  # Click derecho -> siguiente track
                if self.mpris_player:
                    self.mpris_player.next()
                    self.mpris_button.get_child().set_markup(common_text_icons["next"])
                    GLib.timeout_add(500, self._restore_play_pause_icon)
            elif event.button == 2:  # Click medio -> play/pausa
                if self.mpris_player:
                    self.mpris_player.previous()
                    self.mpris_button.get_child().set_markup(common_text_icons["prev"])
                    GLib.timeout_add(500, self._restore_play_pause_icon)
            return True
        return True

    def _restore_play_pause_icon(self):
        self.update_play_pause_icon()
        return False

    def _on_icon_clicked(self, widget):
        if not self.mpris_player:
            return
        # toggle between showing title and artist.
        self._show_artist = not self._show_artist
        text = (
            self.mpris_player.artist
            if self._show_artist and self.mpris_player.artist
            else (
                self.mpris_player.title
                if self.mpris_player.title and self.mpris_player.title.strip()
                else "nothing playing"
            )
        )
        if len(text) > 25:
            text = text[:25] + "..."
        self.mpris_label.set_text(text)

        self.center_stack.set_visible_child(self.mpris_label)

    def update_play_pause_icon(self):
        if self.mpris_player and self.mpris_player.playback_status == "playing":
            self.mpris_button.get_child().set_markup(common_text_icons["pause"])
        else:
            self.mpris_button.get_child().set_markup(common_text_icons["play"])

    def _on_play_pause_clicked(self, button):
        if self.mpris_player:
            self.mpris_player.play_pause()
            self.update_play_pause_icon()

    def _on_mpris_changed(self, *args):
        # update properties when the player's state changes.
        self._apply_mpris_properties()

    def on_player_appeared(self, manager, player):
        # when a new player appears, use it if no player is active.
        if not self.mpris_player and not self.mpris_manager.player_name.startswith(
            "chromium", "firefox"
        ):
            mp = MprisPlayer(player)
            self.mpris_player = mp
            self._apply_mpris_properties()
            self.mpris_player.connect("changed", self._on_mpris_changed)

    def on_player_vanished(self, manager, player_name):
        players = self.mpris_manager.players
        if players and self.mpris_player:
            if players:  # Check if players is not empty after vanishing
                self.current_index = self.current_index % len(players)
                new_player = MprisPlayer(players[self.current_index])
                self.mpris_player = new_player
                self.mpris_player.connect("changed", self._on_mpris_changed)
            else:
                self.mpris_player = None  # No players left
        elif not players:
            self.mpris_player = None
        self._apply_mpris_properties()
