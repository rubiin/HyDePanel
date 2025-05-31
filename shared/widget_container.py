from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.eventbox import EventBox
from fabric.widgets.widget import Widget

from utils.widget_utils import setup_cursor_hover


class ToggleableWidget(Widget):
    """A widget that can be toggled on and off."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def toggle(self):
        """Toggle the visibility of the bar."""
        if self.is_visible():
            self.hide()
        else:
            self.show()


class BoxWidget(Box, ToggleableWidget):
    """A container for box widgets."""

    def __init__(self, spacing=None, style_classes=None, **kwargs):
        # Handle style classes
        all_styles = ["panel-box"]
        if style_classes:
            if isinstance(style_classes, str):
                all_styles.append(style_classes)
            else:
                all_styles.extend(style_classes)

        super().__init__(
            spacing=4 if spacing is None else spacing,
            style_classes=all_styles,
            **kwargs,
        )


class EventBoxWidget(EventBox, ToggleableWidget):
    """A container for box widgets."""

    def __init__(self, config, **kwargs):
        super().__init__(
            style_classes="panel-eventbox",
            **kwargs,
        )
        self.config = config
        self.box = Box(style_classes="panel-box")
        self.children = (self.box,)
        setup_cursor_hover(self)


class ButtonWidget(Button, ToggleableWidget):
    """A container for button widgets. Only used for new widgets that are used on bar"""

    def __init__(self, config, **kwargs):
        super().__init__(
            style_classes="panel-button",
            **kwargs,
        )
        self.box = Box()
        self.children = (self.box,)
        self.config = config

        setup_cursor_hover(self)


class HoverButton(Button):
    """A container for button with hover effects."""

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
        )

        setup_cursor_hover(self)
