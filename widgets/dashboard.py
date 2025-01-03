from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.eventbox import EventBox

from shared.popover import PopOverWindow
from utils.functions import create_scale, text_icon
from utils.widget_config import BarConfig


class DashBoardMenu(Box):
    """A menu to display the weather information."""

    def __init__(self, **kwargs):
        super().__init__(name="dashboard-menu", orientation="v", all_visible=True, **kwargs)

        box1 = CenterBox(
            orientation="v",
            start_children=Box(
                children=(
                    text_icon(
                    "󰃠",
                    props={
                        "style_classes": "panel-text-icon overlay-icon",
                    },
                ),
                create_scale()
                )
            ),
             center_children=Box(
                children=(
                    text_icon(
                    "󰃠",
                    props={
                        "style_classes": "panel-text-icon overlay-icon",
                    },
                ),
                create_scale()
                )
            )
        )

        self.add(box1)


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
