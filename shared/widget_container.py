from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.eventbox import EventBox

from utils.widget_utils import setup_cursor_hover


class BoxWidget(Box):
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


class EventBoxWidget(EventBox):
    """A container for box widgets."""

    def __init__(self, config, **kwargs):
        super().__init__(
            name="panel-eventbox",
            **kwargs,
        )
        setup_cursor_hover(self)


class ButtonWidget(Button):
    """A container for button widgets. Only used for new widgets that are used on bar"""

    def __init__(self, config, **kwargs):
        super().__init__(
            style_classes="panel-button",
            **kwargs,
        )

        setup_cursor_hover(self)

        self.box = Box()
        self.children = (self.box,)
        self.config = config


class HoverButton(Button):
    """A container for button with hover effects."""

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
        )

        setup_cursor_hover(self)
