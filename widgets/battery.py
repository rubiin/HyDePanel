from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.label import Label

from services import battery_service
from shared.widget_container import ButtonWidget
from utils.functions import format_time
from utils.widget_settings import BarConfig


class BatteryWidget(ButtonWidget):
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

        self.box = Box()

        self.children = (self.box,)

        self.client = battery_service

        self.client.connect("changed", lambda *_: self.update_ui())

        self.update_ui()

    def update_ui(self):
        """Update the battery status by fetching the current battery information
        and updating the widget accordingly.
        """
        is_present = self.client.get("IsPresent")

        battery_percent = round(self.client.get("Percentage")) if is_present else 0

        self.battery_label = Label(
            label=f"{battery_percent}%", style_classes="panel-text", visible=False
        )

        battery_state = self.client.get("State")

        is_charging = battery_state == 1 if is_present else False

        temperature = self.client.get("Temperature")

        time_remaining = (
            self.client.get("TimeToFull")
            if is_charging
            else self.client.get("TimeToEmpty")
        )

        self.battery_icon = Image(
            icon_name=self.client.get("IconName"),
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
                self.set_tooltip_text(
                    f"󰄉 Time to full: {format_time(time_remaining)}\n Temperature: {temperature}°C"
                )
            else:
                self.set_tooltip_text(
                    f"󰄉 Time to empty: {format_time(time_remaining)}\n Temperature: {temperature}°C"
                )

        return True
