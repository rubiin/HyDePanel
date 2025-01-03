from fabric.widgets.box import Box
from fabric.widgets.eventbox import EventBox

from shared.animated.scale import AnimatedScale
from shared.popover import PopOverWindow
from utils.functions import text_icon
from utils.widget_config import BarConfig


class DashBoardMenu(Box):
    """A menu to display the weather information."""

    def __init__(self, **kwargs):
        super().__init__(name="dashboard-menu", orientation="v", **kwargs)

        self.children = AnimatedScale(
            marks=None,
            value=70,
            min_value=0,
            max_value=100,
            increments=(1, 1),
            orientation="h",
            h_expand=True,
            h_align="center",
        )


class DashBoardWidget(EventBox):
    """A button to display the date and time."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(name="date-time-button", **kwargs)

        self.config = widget_config["date_time"]

        popup = PopOverWindow(
            parent=bar,
            name="popup",
            child=(DashBoardMenu()),
            visible=False,
            all_visible=False,
        )

        popup.set_pointing_to(self)

        self.children = text_icon(
            "󰃠",
            props={
                "style_classes": "panel-text-icon overlay-icon",
            },
        )

        self.connect(
            "button-press-event",
            lambda *_: popup.set_visible(not popup.get_visible()),
        )
