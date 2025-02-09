import math

from fabric.utils import bulk_connect
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.image import Image
from fabric.widgets.label import Label

from services.power_profile import PowerProfiles
from shared.pop_over import PopOverWindow
from shared.widget_container import ButtonWidget
from utils.functions import format_time
from utils.widget_settings import BarConfig
from utils.widget_utils import psutil_fabricator


class PowerProfileItem(Button):
    """A button to display the power profile."""

    def __init__(
        self,
        key,
        profile,
        active,
        **kwargs,
    ):
        super().__init__(
            **kwargs,
        )
        self.profile = profile

        self.power_profile_service = PowerProfiles().get_initial()

        self.children = (
            Box(
                children=(
                    Image(
                        icon_name=profile["icon_name"],
                        icon_size=15,
                    ),
                    Label(
                        label=profile["name"],
                        style_classes="panel-text",
                    ),
                ),
            ),
        )

        self.connect(
            "button-press-event",
            lambda *_: self.power_profile_service.set_power_profile(key),
        )

        self.add_style_class(
            f"power-profile-button {'active' if key == active else ''}"
        )


class BatteryMenu(Box):
    """A menu to display the battery status."""

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            name="batterymenu",
            orientation="h",
            **kwargs,
        )

        self.power_profile_service = PowerProfiles().get_initial()

        self.profiles = self.power_profile_service.power_profiles

        self.active = self.power_profile_service.get_current_profile()

        self.power_profiles = [
            PowerProfileItem(key=key, profile=profile, active=self.active)
            for key, profile in self.profiles.items()
        ]

        self.children = CenterBox(
            start_children=Box(
                orientation="v",
                spacing=10,
                children=(
                    Label(label="Power Profiles", style_classes="power-profile-title"),
                    Box(
                        orientation="v",
                        spacing=10,
                        style_classes="power-profile-box",
                        children=self.power_profiles,
                    ),
                ),
            )
        )

        self.power_profile_service.connect(
            "profile",
            self.on_profile_changed,
        )

    def on_profile_changed(self, sender, value, *args):
        self.active = value

        for profile in self.power_profiles:
            # Remove the active class from all profiles, before adding to active profile
            profile.get_style_context().remove_class("active")
            profile.add_style_class(
                "active" if profile.profile == self.profiles[self.active] else ""
            )


class Battery(ButtonWidget):
    """A widget to display the current battery status."""

    def __init__(
        self,
        widget_config: BarConfig,
        bar,
        **kwargs,
    ):
        # Initialize the Box with specific name and style
        super().__init__(
            name="battery",
            **kwargs,
        )
        self.config = widget_config["battery"]
        self.full_battery_level = self.config["full_battery_level"]

        bulk_connect(
            self,
            {
                "button-press-event": lambda *_: popup.set_visible(
                    not popup.get_visible()
                ),
            },
        )

        self.box = Box()

        self.children = (self.box,)

        popup = PopOverWindow(
            parent=bar,
            name="battery-menu-popover",
            child=BatteryMenu(),
            visible=False,
            all_visible=False,
        )

        popup.set_pointing_to(self)

        # Set up a repeater to call the update_battery_status method
        psutil_fabricator.connect("changed", self.update_ui)

    def update_ui(self, fabricator, value):
        """Update the battery status by fetching the current battery information
        and updating the widget accordingly.
        """
        # Get the battery status
        battery = value.get("battery")

        if battery is None:
            self.hide()
            return None

        battery_percent = round(battery.percent) if battery else 0

        self.battery_label = Label(
            label=f"{battery_percent}%", style_classes="panel-text", visible=False
        )

        is_charging = battery.power_plugged if battery else False

        self.battery_icon = Image(
            icon_name=self.get_icon_name(
                battery_percent=battery_percent,
                is_charging=is_charging,
            ),
            icon_size=14,
        )

        self.box.children = (self.battery_icon, self.battery_label)

        # Update the label with the battery percentage if enabled
        if self.config["label"]:
            self.battery_label.show()

            ## Hide the label when the battery is full
            if (
                self.config["hide_label_when_full"]
                and battery_percent == self.full_battery_level
            ):
                self.battery_label.hide()

        # Update the tooltip with the battery status details if enabled
        if self.config["tooltip"]:
            if battery_percent == self.full_battery_level:
                self.set_tooltip_text("Full")
            elif is_charging and battery_percent < self.full_battery_level:
                self.set_tooltip_text(f"Time to full: {format_time(battery.secsleft)}")
            else:
                self.set_tooltip_text(f"Time to empty: {format_time(battery.secsleft)}")

        return True

    def get_icon_name(self, battery_percent: int, is_charging: bool):
        """Determine the icon name based on the percentage and charging status."""
        # Determine the icon name based on the battery percentage and charging status
        if battery_percent == self.full_battery_level:
            return "battery-level-100-charged-symbolic"
        icon_level = math.floor(battery_percent / 10) * 10
        return (
            f"battery-level-{icon_level}{'-charging' if is_charging else ''}-symbolic"
        )
