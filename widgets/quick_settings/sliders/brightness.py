from services import Brightness
from shared import SettingSlider
from utils.icons import icons


class BrightnessSlider(SettingSlider):
    """A widget to display a scale for brightness settings."""

    def __init__(
        self,
    ):
        self.client = Brightness()
        super().__init__(
            name="brightness-slider",
            pixel_size=20,
            icon_name=icons["brightness"]["screen"],
        )

        if self.client.screen_brightness == -1:
            self.destroy()
            return

        if self.scale:
            self.scale.connect("change-value", self.on_scale_move)
            self.client.connect("brightness_changed", self.on_brightness_change)

        self.icon_button.connect("clicked", self.reset)

    def reset(self, *_):
        """Reset the brightness to the default value."""
        self.client.screen_brightness = 0

    def on_scale_move(self, _, __, moved_pos):
        self.client.screen_brightness = moved_pos

    def on_brightness_change(self, service: Brightness, _):
        self.scale.set_value(service.screen_brightness)
        # Show percentage in tooltip
        percentage = int((service.screen_brightness / service.max_screen) * 100)
        self.scale.set_tooltip_text(f"{percentage}%")
