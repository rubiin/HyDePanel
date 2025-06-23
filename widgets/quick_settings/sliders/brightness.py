from fabric.utils import cooldown

from services.brightness import BrightnessService
from shared.setting_scale import SettingSlider
from utils.icons import text_icons
from utils.widget_utils import get_brightness_icon_name


class BrightnessSlider(SettingSlider):
    """A widget to display a scale for brightness settings."""

    def __init__(
        self,
    ):
        self.client = BrightnessService()
        super().__init__(
            pixel_size=20,
            icon_name=text_icons["brightness"]["medium"],
            min=0,
            max=self.client.max_screen,  # Use actual max brightness
            start_value=self.client.screen_brightness,
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

    @cooldown(1)
    def on_scale_move(self, _, __, moved_pos):
        self.client.screen_brightness = moved_pos

    def on_brightness_change(self, service: BrightnessService, _):
        brightness_percent = int((service.screen_brightness / service.max_screen) * 100)

        # Avoid unnecessary updates if the value hasn't changed
        if (brightness_percent) == round(self.scale.get_value()):
            return

        self.scale.set_value(brightness_percent)
        self.scale.set_tooltip_text(f"{brightness_percent}%")

        self.update_icon(int(brightness_percent))

    def update_icon(self, current_brightness):
        icon_name = get_brightness_icon_name(current_brightness)["icon_text"]
        self.icon.set_label(icon_name)
