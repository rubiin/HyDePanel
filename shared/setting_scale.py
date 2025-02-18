from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.label import Label

from fabric.widgets.revealer import Revealer
from fabric.widgets.scale import Scale

from shared.widget_container import HoverButton


class SettingSlider(Box):
    """A widget to display a scale for quick settings."""

    def __init__(
        self,
        min: float = 0,
        max: float = 100,
        start_value: float = 50,
        icon_name: str = "package-x-generic-symbolic",
        pixel_size: int = 20,
        display_label=False,
        **kwargs,
    ):
        super().__init__(
            name="setting-slider",
            children=Box(spacing=5, h_expand=True),
            **kwargs,
        )
        self.pixel_size = pixel_size
        self.icon = Image(
            icon_name=icon_name, icon_size=self.pixel_size, style_classes="panel-icon"
        )
        self.icon_button = HoverButton(image=self.icon, name="setting-slider-button")

        self.scale = Scale(
            marks=None,
            min_value=min,
            max_value=max,
            value=start_value,
            increments=(1, 1),
        )

        self.label = Label(
            label=f"{start_value}%", name="setting-slider-label", visible=display_label
        )


        self.scale.connect(
            "change-value",
            lambda _, __, moved_pos: self.label.set_label(f"{round(moved_pos)}%"),
        )

        self.btn = HoverButton(
            image=Image(icon_name="pan-end-symbolic", icon_size=15),
            visible=False,
        )

        self.btn.connect("clicked", lambda _: self.scale.set_value(50))

        self.children = (self.icon_button, self.scale, self.btn)
