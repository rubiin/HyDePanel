from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from fabric.widgets.label import Label

from services.power_profile import PowerProfiles
from shared.submenu import QuickSubMenu, QuickSubToggle


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
            style_classes="submenu-button power-profile",
            **kwargs,
        )
        self.profile = profile
        self.key = key
        self.box = Box(
            orientation="h",
            spacing=10,
            children=(
                Image(
                    icon_name=profile["icon_name"],
                    icon_size=18,
                ),
                Label(
                    label=profile["name"],
                    style_classes="submenu-item-label",
                ),
            ),
        )

        self.power_profile_service = PowerProfiles().get_default()
        self.children = (self.box,)

        self.connect(
            "button-press-event",
            lambda *_: self.power_profile_service.set_power_profile(key),
        )
        self.set_active(active)

    def set_active(self, active):
        if self.key == active:
            self.box.add_style_class("active")
        else:
            self.box.remove_style_class("active")


class PowerProfileSubMenu(QuickSubMenu):
    """A submenu to display power profile options."""

    def __init__(self, **kwargs):
        self.client = PowerProfiles().get_default()
        self.profiles = self.client.power_profiles
        self.active = self.client.get_current_profile()

        self.profile_items = {
            key: PowerProfileItem(key=key, profile=profile, active=self.active)
            for key, profile in self.profiles.items()
        }

        self.scan_button = Button(
            style="background-color: transparent",
        )

        profile_items = list(self.profile_items.values())
        profile_box = Box(
            orientation="v",
            children=profile_items,
            spacing=8,
        )

        super().__init__(
            title="Power profiles",
            title_icon="power-profile-power-saver-symbolic",
            scan_button=self.scan_button,
            child=profile_box,
            **kwargs,
        )

        # Update items when profile changes
        self.client.connect("profile", self.on_profile_changed)

    def on_profile_changed(self, _, profile):
        for item in self.profile_items.values():
            item.set_active(profile)


class PowerProfileToggle(QuickSubToggle):
    """A widget to display a toggle button for Wifi."""

    def __init__(self, submenu: QuickSubMenu, **kwargs):
        super().__init__(
            action_icon="power-profile-power-saver-symbolic",
            action_label="Power Saver",
            submenu=submenu,
            **kwargs,
        )
        self.client = PowerProfiles().get_default()
        self.update_action_button()
        self.set_active_style(True)
        self.action_button.set_sensitive(False)

        self.client.connect(
            "profile",
            self.update_action_button,
        )

    def unslug(self, text):
        return " ".join(word.capitalize() for word in text.split("-"))

    def update_action_button(self, *_):
        self.active_pfl = self.client.get_current_profile()

        icon = self.client.get_profile_icon(self.active_pfl)

        self.action_icon.set_from_icon_name(icon, 18)
        self.set_action_label(self.unslug(self.active_pfl))
