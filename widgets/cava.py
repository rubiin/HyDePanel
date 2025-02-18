from fabric import Fabricator
from fabric.utils import get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.label import Label

from shared.widget_container import ButtonWidget
from utils.widget_settings import BarConfig


class CavaWidget(ButtonWidget):
    """A widget to display the Cava audio visualizer."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(name="cava", **kwargs)

        self.config = widget_config["cava"]

        self.box = Box()

        self.children = self.box

        cava_label = Label(
            v_align="center",
            h_align="center",
        )

        script_path = get_relative_path("../assets/scripts/cava.sh")

        self.box.children = Box(spacing=1, children=[cava_label]).build(
            lambda box, _: Fabricator(
                poll_from=f"bash -c '{script_path} {self.config['bars']}'",
                stream=True,
                on_changed=lambda f, line: cava_label.set_label(line),
            )
        )
