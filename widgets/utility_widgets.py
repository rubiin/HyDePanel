from fabric.widgets.box import Box


class SpacingWidget(Box):
    """A simple widget to add spacing between widgets."""

    def __init__(self, **kwargs):
        super().__init__(name="spacing", **kwargs)


class DividerWidget(Box):
    """A simple widget to add a divider between widgets."""

    def __init__(self, **kwargs):
        super().__init__(name="divider", orientation="vertical", **kwargs)
