import json

from fabric.utils import (
    cooldown,
    exec_shell_command_async,
    get_relative_path,
    invoke_repeater,
)
from fabric.widgets.label import Label
from loguru import logger

from shared import ButtonWidget
from utils import BarConfig, Colors, run_in_thread
from utils.functions import convert_seconds_to_milliseconds
from utils.widget_utils import text_icon


class UpdatesWidget(ButtonWidget):
    """A widget to display the number of available updates."""

    def __init__(
        self,
        widget_config: BarConfig,
        bar,
        **kwargs,
    ):
        # Initialize the EventBox with specific name and style
        super().__init__(widget_config, name="updates", **kwargs)
        self.config = widget_config["updates"]

        script_file = get_relative_path("../assets/scripts/systemupdates.sh")

        self.update_label = Label(label="0", style_classes="panel-text")

        self.base_command = f"{script_file} --{self.config['os']}"

        if self.config["flatpak"]:
            self.base_command += " --flatpak"

        if self.config["snap"]:
            self.base_command += " --snap"

        if self.config["brew"]:
            self.base_command += " --brew"

        if self.config["show_icon"]:
            self.icon = text_icon(
                icon=self.config["icon"],
                props={"style_classes": "panel-icon"},
            )
            self.box.add(self.icon)

        if self.config["label"]:
            self.box.add(self.update_label)

        self.connect("button-press-event", self.on_button_press)

        # Set up a repeater to call the update method at specified intervals
        invoke_repeater(
            convert_seconds_to_milliseconds(self.config["interval"]),
            self.check_update,
            initial_call=True,
        )

    def update_values(self, value: str):
        # Parse the JSON value

        value = json.loads(value)

        # Update the label if enabled
        if self.config["label"]:
            self.update_label.set_label(value["total"])

        # Update the tooltip if enabled
        if self.config["tooltip"]:
            self.set_tooltip_text(value["tooltip"])
        return True

    def on_button_press(self, _, event):
        if event.button == 1:
            self.check_update(update=True)
        else:
            self.check_update()
        return True

    @cooldown(1)
    @run_in_thread
    def check_update(self, update=False):
        # Execute the update script asynchronously and update values

        if update:
            exec_shell_command_async(
                f"{self.base_command} up",
                lambda output: self.update_values(output),
            )
        else:
            logger.info(f"{Colors.INFO}[Updates] Checking for updates...")
            exec_shell_command_async(
                self.base_command,
                lambda output: self.update_values(output),
            )

        return True
