from fabric.utils import exec_shell_command_async

from shared.buttons import QSChevronButton, ScanButton
from shared.submenu import QuickSubMenu
from utils.functions import is_app_running, toggle_command
from utils.widget_utils import (
    create_scale,
    util_fabricator,
)


class HyprSunsetSubMenu(QuickSubMenu):
    """A submenu to display application-specific audio controls."""

    def __init__(self, **kwargs):
        # Create refresh button first since parent needs it
        self.scan_button = ScanButton(visible=False)

        self.scale = create_scale(
            min_value=1000,
            max_value=9000,
            value=6500,
            increments=(100, 100),
        )

        super().__init__(
            title="HyprSunset",
            title_icon="redshift-status-on",
            name="hyprsunset-sub-menu",
            scan_button=self.scan_button,
            child=self.scale,
        )

        if self.scale:
            self.scale.connect("change-value", self.on_scale_move)
            self.update_ui(int(self.scale.get_value()))

    def on_scale_move(self, _, __, moved_pos):
        exec_shell_command_async(
            f"hyprctl hyprsunset temperature {int(moved_pos)}", lambda *_: None
        )
        self.update_ui(int(moved_pos))

        return True

    def update_ui(self, moved_pos):
        """Update the UI elements."""
        # Update the scale value based on the current temperature
        self.scale.set_value(moved_pos)
        self.scale.set_tooltip_text(f"{moved_pos}K")


class HyprSunsetToggle(QSChevronButton):
    """A widget to display a toggle button for Wifi."""

    def __init__(self, submenu: QuickSubMenu, **kwargs):
        super().__init__(
            action_icon="redshift-status-off",
            pixel_size=20,
            action_label="Enabled",
            submenu=submenu,
            **kwargs,
        )
        self.action_button.set_sensitive(True)

        self.connect("action-clicked", self.on_action)

        # reusing the fabricator to call specified intervals
        util_fabricator.connect("changed", self.update_action_button)

    def redlight_temperature(self):
        """Get the redlight temperature from the scale."""
        return int(self.submenu.scale.get_value())

    def on_action(self, *_):
        """Handle the action button click event."""
        toggle_command(
            "hyprsunset",
            full_command=f"hyprsunset -t {self.redlight_temperature()}",
        )
        return True

    def update_action_button(self, *_):
        self.is_running = is_app_running("hyprsunset")
        icon = "redshift-status-on" if self.is_running else "redshift-status-off"

        self.action_icon.set_from_icon_name(icon, 18)
        self.set_action_label("Enabled" if self.is_running else "Disabled")
        if self.is_running:
            self.set_active_style(True)
        else:
            self.set_active_style(False)
