from collections.abc import Iterable
from typing import Literal

from fabric.widgets.widget import Widget
from gi.repository import Gtk


class Grid(Gtk.Grid, Widget):
    """A simple widget to add a grid layout between widgets."""

    def __init__(
        self,
        name: str | None = None,
        visible: bool = True,
        all_visible: bool = False,
        row_spacing: int = 0,
        column_spacing: int = 0,
        style: str | None = None,
        style_classes: Iterable[str] | str | None = None,
        tooltip_text: str | None = None,
        tooltip_markup: str | None = None,
        h_align: Literal["fill", "start", "end", "center", "baseline"]
        | Gtk.Align
        | None = None,
        v_align: Literal["fill", "start", "end", "center", "baseline"]
        | Gtk.Align
        | None = None,
        h_expand: bool = False,
        v_expand: bool = False,
        size: Iterable[int] | int | None = None,
        **kwargs,
    ):
        Gtk.Grid.__init__(self)
        Widget.__init__(
            self,
            name,
            visible,
            all_visible,
            style,
            style_classes,
            tooltip_text,
            tooltip_markup,
            h_align,
            v_align,
            h_expand,
            v_expand,
            size,
            **kwargs,
        )
        self.set_row_spacing(row_spacing)
        self.set_column_spacing(column_spacing)
