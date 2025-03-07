from fabric.utils import exec_shell_command_async, get_relative_path
from gi.repository import Gdk

from shared.widget_container import ButtonWidget
from utils.exceptions import ExecutableNotFoundError
from utils.functions import executable_exists
from utils.widget_settings import BarConfig


class HyprPickerWidget(ButtonWidget):
    """A widget to pick a color."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(name="hypr-picker", **kwargs)

        self.config = widget_config["hypr_picker"]

        self.set_label(f"{self.config['icon']}")

        self.connect("button-press-event", self.on_button_press)

        self.script_file = get_relative_path("../assets/scripts/hyprpicker.sh")

        if not executable_exists("hyprpicker"):
            raise ExecutableNotFoundError("hyprpicker")

        if self.config["tooltip"]:
            self.set_tooltip_text("Pick a color")

    def on_button_press(self, button, event):
        # Mouse event handler
        if event.type == Gdk.EventType.BUTTON_PRESS:
            if event.button == 1:
                # Left click: HEX
                exec_shell_command_async(f"{self.script_file} -hex", lambda *_: None)
            elif event.button == 2:
                # Middle click: HSV
                exec_shell_command_async(f"{self.script_file} -hsv", lambda *_: None)
            elif event.button == 3:
                # Right click: RGB
                exec_shell_command_async(f"{self.script_file} -rgb", lambda *_: None)
