import time
from typing import Literal

from fabric.utils import cooldown, invoke_repeater
from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer
from fabric.widgets.wayland import WaylandWindow as Window
from loguru import logger

import utils.functions as helpers
import utils.icons as icons
from services import Brightness, audio_service
from utils import HyprlandWithMonitors
from utils.types import Keyboard_Mode
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
        self.level = Label(
            name="osd-level", h_align="center", h_expand=True, visible=False
        )
        self.icon = Image(
            icon_name=icons.icons["brightness"]["screen"], icon_size=config["icon_size"]
        )
        self.scale = create_scale()

        self.children = (self.icon, self.scale, self.level)

        if config["percentage"]:
            self.level.set_visible(True)


class BrightnessOSDContainer(GenericOSDContainer):
    """A widget to display the OSD for brightness."""

    def __init__(self, config, **kwargs):
        super().__init__(
            config=config,
            **kwargs,
        )
        self.brightness_service = Brightness()
        self.update_brightness()

        self.brightness_service.connect(
            "brightness_changed", self.on_brightness_changed
        )

    @cooldown(0.1)
    def update_brightness(self):
        normalized_brightness = helpers.convert_to_percent(
            self.brightness_service.screen_brightness,
            self.brightness_service.max_screen,
        )
        self.update_icon(int(normalized_brightness))

    def update_icon(self, current_brightness):
        icon_name = get_brightness_icon_name(current_brightness)["icon"]
        self.level.set_label(f"{current_brightness}%")
        self.icon.set_from_icon_name(icon_name)
        self.scale.set_value(current_brightness)

    def on_brightness_changed(self, sender, value, *args):
        self.update_brightness()


class AudioOSDContainer(GenericOSDContainer):
    """A widget to display the OSD for audio."""

    def __init__(self, config, **kwargs):
        super().__init__(
            config=config,
            **kwargs,
        )
        self.audio_service = audio_service

        self.update_volume()

        self.audio_service.connect("notify::speaker", self.on_audio_speaker_changed)

    def on_volume_changed(self, *_):
        self.update_volume()

    def on_audio_speaker_changed(self, *_):
        if self.audio_service.speaker:
            self.audio_service.speaker.connect("notify::volume", self.on_volume_changed)
            self.update_volume()
        return True

    def update_volume(self):
        if self.audio_service.speaker and not self.is_hovered():
            volume = round(self.audio_service.speaker.volume)
            is_over_amplified = volume > 100
            scaled_volume = volume - 100 if is_over_amplified else volume

            self.scale.set_value(scaled_volume)
            self.level.set_label(f"{volume}%")
            self.update_icon(volume)

            if is_over_amplified:
                self.scale.add_style_class("overamplified")
            else:
                self.scale.remove_style_class("overamplified")

    def update_icon(self, volume):
        icon_name = get_audio_icon_name(volume, self.audio_service.speaker.muted)[
            "icon"
        ]
        self.icon.set_from_icon_name(icon_name)


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

        self.last_activity_time = time.time()

        audio_service = self.audio_container.audio_service

        def on_audio_speaker_changed(*_):
            if audio_service.speaker:
                audio_service.speaker.connect("notify::volume", self.show_audio)

        self.brightness_container.brightness_service.connect(
            "brightness_changed",
            self.show_brightness,
        )
        audio_service.connect("notify::speaker", on_audio_speaker_changed)

        invoke_repeater(100, self.check_inactivity, initial_call=True)

    def show_audio(self, *_):
        logger.debug("Audio changed,showing audio OSD")
        self.show_box(box_to_show="audio")

    def show_brightness(self, *_):
        logger.debug("Brightness changed,showing brightness OSD")
        self.show_box(box_to_show="brightness")

    def show_box(self, box_to_show: Literal["audio", "brightness"]):
        if box_to_show == "audio":
            self.revealer.children = self.audio_container
        elif box_to_show == "brightness":
            self.revealer.children = self.brightness_container
        self.set_visible(True)
        self.revealer.set_reveal_child(True)
        self.reset_inactivity_timer()

    def start_hide_timer(self):
        self.set_visible(False)

    def reset_inactivity_timer(self):
        self.last_activity_time = time.time()

    def check_inactivity(self):
        if time.time() - self.last_activity_time >= (self.timeout / 1000):
            self.start_hide_timer()
        return True
