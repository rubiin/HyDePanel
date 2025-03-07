from fabric.utils import exec_shell_command_async, get_relative_path

from shared.widget_container import ButtonWidget
from utils.widget_settings import BarConfig


class OCRWidget(ButtonWidget):
    """A widget to pick a color."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(name="ocr", **kwargs)

        self.config = widget_config["ocr"]

        self.set_label(f"{self.config['icon']}")

        self.connect(
            "button-press-event",
            lambda *_: exec_shell_command_async(f"{self.script_file}", lambda *_: None),
        )

        self.script_file = get_relative_path("../assets/scripts/ocr.sh")

        if self.config["tooltip"]:
            self.set_tooltip_text("Click to ocr")
