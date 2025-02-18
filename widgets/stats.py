from fabric.widgets.box import Box
from fabric.widgets.label import Label

import utils.functions as helpers
from shared.widget_container import ButtonWidget
from utils.icons import common_text_icons
from utils.widget_settings import BarConfig
from utils.widget_utils import psutil_fabricator, text_icon


class CpuWidget(ButtonWidget):
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

        self.box = Box()
        self.children = (self.box,)

        self.config = widget_config["cpu"]

        # Create a TextIcon with the specified icon and size
        self.text_icon = text_icon(
            icon=self.config["icon"],
            size=self.config["icon_size"],
            props={"style_classes": "panel-icon"},
        )

        self.cpu_level_label = Label(
            label="0%", style_classes="panel-text", visible=False
        )

        self.box.children = (self.text_icon, self.cpu_level_label)

        # Set up a fabricator to call the update_label method when the CPU usage changes
        psutil_fabricator.connect("changed", self.update_ui)

    def update_ui(self, _, value):
        # Update the label with the current CPU usage if enabled
        avg_usage = value.get("cpu_freq")
        if self.config["label"]:
            self.cpu_level_label.show()
            self.cpu_level_label.set_label(value.get("cpu_usage"))

        # Update the tooltip with the memory usage details if enabled
        if self.config["tooltip"]:
            tooltip_text = ""

            for key, value in enumerate(avg_usage):
                tooltip_text += f"core{key}: {round(value.current)} Mhz\n"

            self.set_tooltip_text(tooltip_text)

        return True


class MemoryWidget(ButtonWidget):
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

        self.box = Box()
        self.children = (self.box,)

        # Create a TextIcon with the specified icon and size
        self.icon = text_icon(
            icon=self.config["icon"],
            size=self.config["icon_size"],
            props={"style_classes": "panel-icon"},
        )
        self.memory_level_label = Label(
            label="0%", style_classes="panel-text", visible=False
        )

        self.box.children = (self.icon, self.memory_level_label)

        # Set up a fabricator to call the update_label method  at specified intervals
        psutil_fabricator.connect("changed", self.update_ui)

    def update_ui(self, _, value):
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
                f"󰾆 {self.percent_used}%\n{common_text_icons['memory']} {self.ratio()}",
            )

        return True

    def get_used(self):
        return helpers.convert_bytes(self.used_memory, "gb")

    def get_total(self):
        return helpers.convert_bytes(self.total_memory, "gb")

    def ratio(self):
        return f"{self.get_used()}/{self.get_total()}"


class StorageWidget(ButtonWidget):
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

        self.box = Box()
        self.children = (self.box,)

        # Create a TextIcon with the specified icon and size
        self.icon = text_icon(
            icon=self.config["icon"],
            size=self.config["icon_size"],
            props={"style_classes": "panel-icon"},
        )

        self.storage_level_label = Label(
            label="0", style_classes="panel-text", visible=False
        )

        self.box.children = (self.icon, self.storage_level_label)

        # Set up a fabricator to call the update_label method at specified intervals
        psutil_fabricator.connect("changed", self.update_ui)

    def update_ui(self, _, value):
        # Get the current disk usage
        self.disk = value.get("disk")

        # Update the label with the used storage if enabled
        if self.config["label"]:
            self.storage_level_label.set_label(f"{self.get_used()}")
            self.storage_level_label.show()

        # Update the tooltip with the storage usage details if enabled
        if self.config["tooltip"]:
            self.set_tooltip_text(
                f"󰾆 {self.disk.percent}%\n{common_text_icons['storage']} {self.ratio()}"
            )

        return True

    def get_used(self):
        return helpers.convert_bytes(self.disk.used, "gb")

    def get_total(self):
        return helpers.convert_bytes(self.disk.total, "gb")

    def ratio(self):
        return f"{self.get_used()}/{self.get_total()}"
