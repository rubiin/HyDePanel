from shared.buttons import QSChevronButton, ScanButton
from shared.submenu import QuickSubMenu


class HyprSunsetSubMenu(QuickSubMenu):
    """A submenu to display application-specific audio controls."""

    def __init__(self, **kwargs):
        # Create refresh button first since parent needs it
        self.scan_button = ScanButton(visible=False)

        super().__init__(
            title="HyprSunset",
            title_icon="redshift-status-on",
            name="hyprsunset-sub-menu",
            scan_button=self.scan_button,
            child=self.scan_button,
            **kwargs,
        )


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
