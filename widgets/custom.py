from fabric.utils import exec_shell_command_async
from fabric.widgets.box import Box
from fabric.widgets.label import Label

from shared import ButtonWidget
from utils import BarConfig
from utils.widget_utils import text_icon, util_fabricator


class CustomWidget(ButtonWidget):
    """A widget to count the number of clicks."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(widget_config, name="custom_widget", **kwargs)
        self.config = widget_config["custom_widget"]

        # Create a TextIcon with the specified icon and size
        self.text_icon = text_icon(
            icon=self.config["icon"],
            props={"style_classes": "panel-icon"},
        )

        self.label = Label(label="0%", style_classes="panel-text", visible=True)

        self.box = Box()

        self.box.children = (self.text_icon, self.label)

        # Set up a fabricator to call the update_label method when the CPU usage changes
        util_fabricator.connect("changed", self.update_ui)

    def update_ui(self, fabricator, value):
        # Update the label with the current CPU usage if enabled
        exec_shell_command_async(
            self.config["command"], lambda x: self.label.set_label(x)
        )

        return True
