from time import sleep

from fabric import Fabricator

from services import audio_service
from shared.setting_scale import SettingSlider
from utils.icons import icons


class AudioSlider(SettingSlider):
    """A widget to display a scale for audio settings."""

    def __init__(self):
        self.client = audio_service

        super().__init__(
            icon_name=icons["audio"]["volume"]["high"], display_buttons=True
        )
        self.scale.connect("change-value", self.on_scale_move)
        self.client.connect("speaker-changed", self.on_speaker_change)
        self.icon_button.connect("clicked", self.on_button_click)

        def applications_poll(_):
            while True:
                yield self.client.applications
                sleep(1)

        self.applications_fabricator = Fabricator(
            poll_from=applications_poll, stream=True
        )

        self.applications_fabricator.connect("changed", self.change_applications)

    def on_scale_move(self, _, __, moved_pos):
        self.client.speaker.volume = moved_pos

    def on_speaker_change(self, *args):
        self.scale.set_sensitive(not audio_service.speaker.muted)
        self.scale.set_value(audio_service.speaker.volume)
        self.label.set_label(f"{round(audio_service.speaker.volume)}%")

    def on_button_click(self, *_):
        self.client.speaker.muted = not self.client.speaker.muted

    def change_applications(self, _, value):
        self.btn.set_visible(len(value) > 0)
