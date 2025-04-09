import subprocess

from fabric.widgets.label import Label

import utils.functions as helpers
from utils import ExecutableNotFoundError
from utils.widget_utils import (
    text_icon,
    util_fabricator,
)

from .widget_container import ButtonWidget


class CommandSwitcher(ButtonWidget):
    """A button widget to toggle a command.
    Useful for making services with two states."""

    def __init__(
        self,
        command: str,
        enabled_icon: str,
        disabled_icon: str,
        name: str,
        label=True,
        tooltip=True,
        config=None,
        style_classes: str = "",
        **kwargs,
    ):
        self.command = command
        self.command_without_args = self.command.split(" ")[0]  # command without args

        super().__init__(
            config,
            name=name,
            **kwargs,
        )

        if not helpers.executable_exists(self.command_without_args):
            raise ExecutableNotFoundError(self.command_without_args)

        self.add_style_class(style_classes)

        self.enabled_icon = enabled_icon
        self.disabled_icon = disabled_icon
        self.label = label
        self.tooltip = tooltip

        self.icon = text_icon(
            icon=enabled_icon,
            props={"style_classes": "panel-icon"},
        )

        self.label_text = Label(
            visible=False,
            label="Enabled",
            style_classes="panel-text",
        )

        self.box.children = (self.icon, self.label_text)

        self.connect("clicked", self.toggle)

        # reusing the fabricator to call specified intervals
        util_fabricator.connect("changed", lambda *_: self.update_ui())

    def toggle(self, *_):
        is_app_running = helpers.is_app_running(self.command_without_args)

        if is_app_running:
            helpers.kill_process(self.command_without_args)
        else:
            subprocess.Popen(
                self.command.split(" "),
                stdin=subprocess.DEVNULL,  # No input stream
                stdout=subprocess.DEVNULL,  # Optionally discard the output
                stderr=subprocess.DEVNULL,  # Optionally discard the error output
                start_new_session=True,  # This prevents the process from being killed
            )

        self.update_ui()
        return True

    def update_ui(self):
        is_app_running = helpers.is_app_running(self.command_without_args)

        if is_app_running:
            self.add_style_class("active")
        else:
            self.remove_style_class("active")

        if self.label:
            self.label_text.set_visible(True)
            self.label_text.set_label("Enabled" if is_app_running else "Disabled")

        self.icon.set_label(self.enabled_icon if is_app_running else self.disabled_icon)

        if self.tooltip:
            self.set_tooltip_text(
                f"{self.command_without_args} enabled"
                if is_app_running
                else f"{self.command_without_args} disabled",
            )
        return True
