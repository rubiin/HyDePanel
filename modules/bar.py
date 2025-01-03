from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.wayland import WaylandWindow

from utils.widget_config import widget_config
from widgets import (
    Battery,
    BlueToothWidget,
    BrightnessWidget,
    CpuWidget,
    DateTimeWidget,
    HyprIdleWidget,
    HyprSunsetWidget,
    KeyboardLayoutWidget,
    LanguageWidget,
    MemoryWidget,
    Mpris,
    PowerButton,
    Recorder,
    StorageWidget,
    SystemTray,
    TaskBarWidget,
    ThemeSwitcherWidget,
    UpdatesWidget,
    VolumeWidget,
    WeatherWidget,
    WindowTitleWidget,
    WorkSpacesWidget,
)
from widgets.dashboard import DashBoardWidget


class StatusBar(WaylandWindow):
    """A widget to display the status bar panel."""

    def __init__(self, **kwargs):
        self.widgets_list = {
            "battery": Battery,
            "bluetooth": BlueToothWidget,
            "brightness": BrightnessWidget,
            "cpu": CpuWidget,
            "date_time": DateTimeWidget,
            "hypr_idle": HyprIdleWidget,
            "hypr_sunset": HyprSunsetWidget,
            "keyboard": KeyboardLayoutWidget,
            "language": LanguageWidget,
            "dashboard": DashBoardWidget,
            "memory": MemoryWidget,
            "mpris": Mpris,
            "power": PowerButton,
            "recorder": Recorder,
            "storage": StorageWidget,
            "system_tray": SystemTray,
            "task_bar": TaskBarWidget,
            "theme_switcher": ThemeSwitcherWidget,
            "updates": UpdatesWidget,
            "volume": VolumeWidget,
            "weather": WeatherWidget,
            "window_title": WindowTitleWidget,
            "workspaces": WorkSpacesWidget,
        }

        layout = self.make_layout()

        box = CenterBox(
            name="panel-inner",
            start_children=Box(
                spacing=4,
                orientation="h",
                children=layout["left_section"],
            ),
            center_children=Box(
                spacing=4,
                orientation="h",
                children=layout["middle_section"],
            ),
            end_children=Box(
                spacing=4,
                orientation="h",
                children=layout["right_section"],
            ),
        )
        super().__init__(
            name="panel",
            layer="top",
            anchor="left top right",
            pass_through=False,
            exclusivity="auto",
            visible=True,
            all_visible=False,
            child=box,
            **kwargs,
        )

    def make_layout(self):
        """assigns the three sections their respective widgets"""

        layout = {"left_section": [], "middle_section": [], "right_section": []}

        for key in layout:
            layout[key].extend(
                self.widgets_list[widget](widget_config, bar=self)
                for widget in widget_config["layout"][key]
            )

        return layout
