from fabric.hyprland.widgets import get_hyprland_connection
from fabric.widgets.label import Label
from loguru import logger

from shared import ButtonWidget
from utils import BarConfig
from utils.widget_utils import text_icon


class SubMapWidget(ButtonWidget):
    """A widget to display the current submap."""

    def __init__(self, widget_config: BarConfig, **kwargs):
        super().__init__(widget_config["submap"], name="submap", **kwargs)

        self.submap_label = Label(label="0", style_classes="panel-text")

        if self.config["show_icon"]:
            # Create a TextIcon with the specified icon and size
            self.icon = text_icon(
                icon=self.config["icon"],
                props={"style_classes": "panel-icon"},
            )
            self.box.add(self.icon)

        self.box.add(self.submap_label)

        self.connection = get_hyprland_connection()

        self.connection.connect("event::submap", self.get_submap)

        # all aboard...
        if self.connection.ready:
            self.on_ready(None)
        else:
            self.connection.connect("event::ready", self.on_ready)

    def on_ready(self, _):
        return self.get_submap(), logger.info(
            "[Submap] Connected to the hyprland socket"
        )

    def get_submap(self, *_):
        submap = str(self.connection.send_command("submap").reply.decode()).strip("\n")
        if self.config["label"]:
            self.submap_label.set_visible(True)

        if submap == "unknown request":
            submap = "default"

        self.submap_label.set_label(submap)

        if self.config["tooltip"]:
            self.set_tooltip_text(
                f"Current submap: {submap}",
            )
