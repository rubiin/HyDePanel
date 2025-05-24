from typing import ClassVar, Literal

from fabric.utils import cooldown
from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer
from fabric.widgets.wayland import WaylandWindow as Window
from gi.repository import GLib, GObject

from services import Brightness, audio_service
from utils import HyprlandWithMonitors, Keyboard_Mode, symbolic_icons
from utils.widget_utils import (
    create_scale,
    get_audio_icon_name,
    get_brightness_icon_name,
)


class GenericOSDContainer(Box):
    """A generic OSD container to display the OSD for brightness and audio."""

    def __init__(self, config, **kwargs):
        super().__init__(
            orientation="h",
            spacing=10,
            name="osd-container",
            **kwargs,
        )

        self.icon = Image(
            icon_name=symbolic_icons["brightness"]["screen"],
            icon_size=config["icon_size"],
        )
        self.scale = create_scale(
            name="osd-scale",
        )

        self.children = (self.icon, self.scale)

        if config["percentage"]:
            self.level = Label(name="osd-level", h_align="center", h_expand=True)
            self.add(self.level)


class BrightnessOSDContainer(GenericOSDContainer):
    """A widget to display the OSD for brightness."""

    __gsignals__: ClassVar = {
        "brightness-changed": (GObject.SignalFlags.RUN_FIRST, None, (int,))
    }

    def __init__(self, config, **kwargs):
        super().__init__(
            config=config,
            **kwargs,
        )
        self.brightness_service = Brightness()
        self.config = config
        self.update_brightness()

        self.brightness_service.connect(
            "brightness_changed", self.on_brightness_changed
        )

    @cooldown(0.1)
    def update_brightness(self):
        brightness_percent = self.brightness_service.screen_brightness_percentage
        self.level.set_label(f"{round(brightness_percent)}%")
        self.scale.set_value(round(brightness_percent))
        self.update_icon(int(brightness_percent))

    def update_icon(self, current_brightness):
        icon_name = get_brightness_icon_name(current_brightness)["icon"]
        self.icon.set_from_icon_name(icon_name, self.config["icon_size"])

    def on_brightness_changed(self, service, value):
        self.update_brightness()
        self.emit("brightness-changed", 0)


class AudioOSDContainer(GenericOSDContainer):
    """A widget to display the OSD for audio."""

    __gsignals__: ClassVar = {
        "volume-changed": (GObject.SignalFlags.RUN_FIRST, None, ())
    }

    def __init__(self, config, **kwargs):
        super().__init__(
            config=config,
            **kwargs,
        )
        self.audio_service = audio_service

        self.config = config

        self.audio_service.connect("notify::speaker", self.on_speaker_changed)
        self.audio_service.connect("changed", self.check_mute)

    @cooldown(0.1)
    def check_mute(self, audio):
        if not audio.speaker:
            return
        if audio.speaker.muted:
            self.update_icon(0)
            self.emit("volume-changed")
        else:
            self.update_icon(audio.speaker.volume)

    def on_speaker_changed(self, audio, _):
        if speaker := self.audio_service.speaker:
            speaker.connect("notify::volume", self.update_volume)

    @cooldown(0.1)
    def update_volume(self, speaker, _):
        speaker.handler_block_by_func(self.update_volume)
        self.emit(
            "volume-changed",
        )
        if not self.audio_service.speaker:
            return

        volume = round(self.audio_service.speaker.volume)

        is_over_amplified = volume > 100

        self.scale.add_style_class(
            "overamplified"
        ) if is_over_amplified else self.scale.remove_style_class("overamplified")

        if self.audio_service.speaker.muted:
            self.update_icon(0)
        else:
            self.update_icon(volume)

        self.scale.set_value(volume)
        self.level.set_label(f"{volume}%")
        speaker.handler_unblock_by_func(self.update_volume)

    def update_icon(self, volume):
        icon_name = get_audio_icon_name(volume, self.audio_service.speaker.muted)[
            "icon"
        ]
        self.icon.set_from_icon_name(icon_name, self.config["icon_size"])


class OSDContainer(Window):
    """A widget to display the OSD for audio and brightness."""

    def __init__(
        self,
        config,
        transition_duration=200,
        keyboard_mode: Keyboard_Mode = "none",
        **kwargs,
    ):
        self.config = config["modules"]["osd"]

        self.audio_container = AudioOSDContainer(config=self.config)
        self.brightness_container = BrightnessOSDContainer(config=self.config)

        self.timeout = self.config["timeout"]

        self.revealer = Revealer(
            name="osd-revealer",
            transition_type="slide-right",
            transition_duration=transition_duration,
            child_revealed=False,
        )

        super().__init__(
            layer="overlay",
            anchor=self.config["anchor"],
            child=self.revealer,
            visible=False,
            pass_through=True,
            keyboard_mode=keyboard_mode,
            **kwargs,
        )

        self.monitor = HyprlandWithMonitors().get_current_gdk_monitor_id()

        self.hide_timer_id = None
        self.suppressed: bool = False

        self.audio_container.connect("volume-changed", self.show_audio)

        self.brightness_container.connect("brightness-changed", self.show_brightness)

    def show_audio(self, *_):
        self.show_box(box_to_show="audio")

    def show_brightness(self, *_):
        self.show_box(box_to_show="brightness")

    def show_box(self, box_to_show: Literal["audio", "brightness"]):
        if self.suppressed:
            return

        if box_to_show == "audio":
            self.revealer.children = self.audio_container
        elif box_to_show == "brightness":
            self.revealer.children = self.brightness_container
        self.revealer.set_reveal_child(True)

        self.set_visible(True)

        if self.hide_timer_id is not None:
            GLib.source_remove(self.hide_timer_id)

        self.hide_timer_id = GLib.timeout_add(self.timeout, self._hide)

    def _hide(self):
        self.set_visible(False)
        self.hide_timer_id = None
        return False
