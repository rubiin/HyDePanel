import datetime

from fabric.widgets.box import Box
from fabric.widgets.datetime import DateTime


class DateTimeBox(Box):
    """A widget to display the current date and time."""

    def __init__(self, **kwargs):
        super().__init__(name="date-time", style_classes="panel-box", **kwargs)

        # Get current date and time
        now = datetime.datetime.now()

        self.date_time = DateTime()
        self.children = self.date_time
        self.set_tooltip_text(now.strftime("%Y-%m-%d %H:%M:%S"))
