from fabric.utils import exec_shell_command_async, get_relative_path, invoke_repeater
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.wayland import WaylandWindow

from utils.functions import convert_seconds_to_milliseconds
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
    NetStatWidget,
    WorkSpacesWidget,
)


class StatusBar(WaylandWindow):
    """A widget to display the status bar panel."""

    def check_for_bar_updates(self):
        exec_shell_command_async(
            get_relative_path("../assets/scripts/barupdate.sh"),
            lambda _: None,
        )
        return True

    def __init__(self, **kwargs):
        self.widgets_list = {
            "battery": Battery,
            "netstat": NetStatWidget,
            "bluetooth": BlueToothWidget,
            "brightness": BrightnessWidget,
            "cpu": CpuWidget,
            "date_time": DateTimeWidget,
            "hypr_idle": HyprIdleWidget,
            "hypr_sunset": HyprSunsetWidget,
            "keyboard": KeyboardLayoutWidget,
            "language": LanguageWidget,
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

        if widget_config["options"]["check_updates"]:
            invoke_repeater(
                convert_seconds_to_milliseconds(3600),
                self.check_for_bar_updates,
                initial_call=True,
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
