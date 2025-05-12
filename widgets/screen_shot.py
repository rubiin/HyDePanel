from fabric.widgets.label import Label

from services.screen_record import ScreenRecorder
from shared import ButtonWidget
from utils import BarConfig
from utils.widget_utils import text_icon


# todo check children
class ScreenShotWidget(ButtonWidget):
    """A widget to switch themes."""

    def __init__(self, widget_config: BarConfig, **kwargs):
        super().__init__(widget_config["screen_shot"], name="screen_shot", **kwargs)

        if self.config["tooltip"]:
            self.set_tooltip_text("Screen Shot")

        self.recorder_service = ScreenRecorder()

        self.screenshot_label = Label(label="0", style_classes="panel-text")

        self.children = text_icon(
            self.config["icon"],
            props={"style_classes": "panel-icon"},
        )

        self.connect("clicked", self.handle_click)

    def handle_click(self, *_):
        """Start recording the screen."""
        self.recorder_service.start_recording(path=self.config["path"])
