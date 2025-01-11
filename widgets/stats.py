from fabric.widgets.label import Label

import utils.functions as helpers
from shared.widget_container import BoxWidget
from utils.icons import common_text_icons
from utils.widget_config import BarConfig
from fabric.hyprland.service import Hyprland as HyprlandService, HyprlandEvent


class CpuWidget(BoxWidget):
    """A widget to display the current CPU usage."""

    def __init__(
        self,
        widget_config: BarConfig,
        **kwargs,
    ):
        # Initialize the Box with specific name and style
        super().__init__(
            name="cpu",
            **kwargs,
        )

        self.config = widget_config["cpu"]

        # Create a TextIcon with the specified icon and size
        self.text_icon = helpers.text_icon(
            icon=self.config["icon"],
            size=self.config["icon_size"],
            props={"style_classes": "panel-text-icon"},
        )

        self.cpu_level_label = Label(
            label="0%", style_classes="panel-text", visible=False
        )

        self.children = (self.text_icon, self.cpu_level_label)

        # Set up a fabricator to call the update_label method when the CPU usage changes
        helpers.psutil_fabricator.connect("changed", self.update_ui)

    def update_ui(self, fabricator, value):
        # Update the label with the current CPU usage if enabled
        if self.config["label"]:
            self.cpu_level_label.show()
            self.cpu_level_label.set_label(value.get("cpu_usage"))

        return True


class MemoryWidget(BoxWidget):
    """A widget to display the current memory usage."""

    def __init__(
        self,
        widget_config: BarConfig,
        **kwargs,
    ):
        # Initialize the Box with specific name and style
        super().__init__(
            name="memory",
            **kwargs,
        )

        self.config = widget_config["memory"]

        # Create a TextIcon with the specified icon and size
        self.icon = helpers.text_icon(
            icon=self.config["icon"],
            size=self.config["icon_size"],
            props={"style_classes": "panel-text-icon"},
        )
        self.memory_level_label = Label(
            label="0%", style_classes="panel-text", visible=False
        )

        self.children = (self.icon, self.memory_level_label)

        # Set up a fabricator to call the update_label method  at specified intervals
        helpers.psutil_fabricator.connect("changed", self.update_ui)

    def update_ui(self, fabricator, value):
        # Get the current memory usage
        memory = value.get("memory")
        self.used_memory = memory.used
        self.total_memory = memory.total
        self.percent_used = memory.percent

        # Update the label with the used memory if enabled
        if self.config["label"]:
            self.memory_level_label.set_label(self.get_used())
            self.memory_level_label.show()

        # Update the tooltip with the memory usage details if enabled
        if self.config["tooltip"]:
            self.set_tooltip_text(
                f"󰾆 {self.percent_used}%\n{common_text_icons['memory']} {self.get_used()}/{self.get_total()}",
            )

        return True

    def get_used(self):
        return helpers.convert_bytes(self.used_memory, "gb")

    def get_total(self):
        return helpers.convert_bytes(self.total_memory, "gb")


class StorageWidget(BoxWidget):
    """A widget to display the current storage usage."""

    def __init__(
        self,
        widget_config: BarConfig,
        **kwargs,
    ):
        # Initialize the Box with specific name and style
        super().__init__(
            name="storage",
            **kwargs,
        )
        self.config = widget_config["storage"]

        # Create a TextIcon with the specified icon and size
        self.icon = helpers.text_icon(
            icon=self.config["icon"],
            size=self.config["icon_size"],
            props={"style_classes": "panel-text-icon"},
        )

        self.storage_level_label = Label(
            label="0", style_classes="panel-text", visible=False
        )

        self.children = (self.icon, self.storage_level_label)

        # Set up a fabricator to call the update_label method at specified intervals
        helpers.psutil_fabricator.connect("changed", self.update_ui)

    def update_ui(self, fabricator, value):
        # Get the current disk usage
        self.disk = value.get("disk")

        # Update the label with the used storage if enabled
        if self.config["label"]:
            self.storage_level_label.set_label(f"{self.get_used()}")
            self.storage_level_label.show()

        # Update the tooltip with the storage usage details if enabled
        if self.config["tooltip"]:
            self.set_tooltip_text(
                f"󰾆 {self.disk.percent}%\n{common_text_icons['storage']} {self.get_used()}/{self.get_total()}",
            )

        return True

    def get_used(self):
        return helpers.convert_bytes(self.disk.used, "gb")

    def get_total(self):
        return helpers.convert_bytes(self.disk.total, "gb")


class NetStatWidget(BoxWidget):
    """A widget to display the current CPU usage."""

    def __init__(
        self,
        widget_config: BarConfig,
        **kwargs,
    ):
        # Initialize the Box with specific name and style
        super().__init__(
            name="netstat",
            **kwargs,
        )

        self.config = widget_config["netstat"]

        # Create a TextIcon with the specified icon and size
        self.text_icon = helpers.text_icon(
            icon=self.config["icon"],
            size=self.config["icon_size"],
            props={"style_classes": "panel-text-icon"},
        )

        self.net_stat_label = Label(
            label="0%", style_classes="panel-text", visible=False
        )

        self.children = (self.text_icon, self.net_stat_label)

        # Set up a fabricator to call the update_label method when the CPU usage changes
        helpers.psutil_fabricator.connect("changed", self.update_ui)

    def update_ui(self, fabricator, value):
        # Update the label with the current CPU usage if enabled
        netstat = value.get("nestat")
        text = f" {helpers.convert_bytes(round(netstat.bytes_recv), to='mb', unit=False)} MB/s  {helpers.convert_bytes(round(netstat.bytes_sent), to='mb', unit=False)} MB/s"
        if self.config["label"]:
            self.net_stat_label.show()
            self.net_stat_label.set_label(text)

        return True


class SubmapWidget(BoxWidget):
    """A widget to display the current submap."""

    def __init__(
        self,
        widget_config: BarConfig,
        **kwargs,
    ):
        # Initialize the Box with specific name and style
        super().__init__(
            name="submap",
            **kwargs,
        )

        self.config = widget_config["netstat"]

        # Create a TextIcon with the specified icon and size
        self.icon = helpers.text_icon(
            icon=self.config["icon"],
            size=self.config["icon_size"],
            props={"style_classes": "panel-text-icon"},
        )

        self.submap_label = Label(label="0", style_classes="panel-text", visible=False)

        self.children = (self.icon, self.submap_label)

        HyprlandService.connect("submap::changed", self.update_ui)

    def update_ui(self, _, event: HyprlandEvent):
        # Update the label with the used storage if enabled
        if self.config["label"]:
            self.submap_label.set_label(event.data)
            self.submap_label.show()

        # Update the tooltip with the storage usage details if enabled
        if self.config["tooltip"]:
            self.set_tooltip_text(
                "",
            )

        return True
