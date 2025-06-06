import time
from typing import List

from fabric.notifications import Notification
from fabric.utils import bulk_connect
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.datetime import DateTime
from fabric.widgets.eventbox import EventBox
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer
from fabric.widgets.scrolledwindow import ScrolledWindow
from gi.repository import GdkPixbuf, GLib, Gtk
from loguru import logger

import utils.constants as constants
import utils.functions as helpers
from services import notification_service
from shared import ButtonWidget, Popover, Separator
from shared.circle_image import CircleImage
from shared.widget_container import HoverButton
from utils import BarConfig, Colors
from utils.functions import uptime
from utils.icons import icons
from utils.widget_utils import get_icon, util_fabricator


class DateMenuNotification(EventBox):
    """A widget to display a notification."""

    def __init__(
        self,
        id: int,
        notification: Notification,
        **kwargs,
    ):
        super().__init__(
            size=(constants.NOTIFICATION_WIDTH, -1),
            name="datemenu-notification-eventbox",
            pass_through=True,
            **kwargs,
        )

        self._notification = notification
        self._id = id

        self._timeout_id = None

        self.notification_box = Box(
            spacing=8,
            name="notification",
            h_expand=True,
            orientation="v",
            style="border: 0;",
        )

        self.revealer = Revealer(
            name="notification-revealer",
            transition_type="slide-up",
            transition_duration=400,
            child=self.notification_box,
            child_revealed=True,
        )

        header_container = Box(
            spacing=8, orientation="h", style_classes="notification-header"
        )

        header_container.children = (
            get_icon(notification.app_icon),
            Label(
                markup=helpers.parse_markup(
                    str(
                        self._notification.summary
                        if self._notification.summary
                        else notification.app_name,
                    )
                ),
                h_align="start",
                h_expand=True,
                line_wrap="word-char",
                style_classes="summary",
                style="font-size: 13.5px;",
            ),
        )
        self.close_button = Button(
            style_classes="close-button",
            image=Image(
                name="close-icon",
                icon_name=helpers.check_icon_exists(
                    icons["ui"]["close"],
                    icons["ui"]["window_close"],
                ),
                icon_size=16,
            ),
            on_clicked=self.clear_notification,
        )

        header_container.pack_end(
            Box(v_align="start", children=(self.close_button)),
            False,
            False,
            0,
        )

        body_container = Box(
            spacing=15, orientation="h", style_classes="notification-body"
        )

        try:
            if image_pixbuf := self._notification.image_pixbuf:
                body_container.add(
                    CircleImage(
                        pixbuf=image_pixbuf.scale_simple(
                            constants.NOTIFICATION_IMAGE_SIZE,
                            constants.NOTIFICATION_IMAGE_SIZE,
                            GdkPixbuf.InterpType.BILINEAR,
                        ),
                        size=constants.NOTIFICATION_IMAGE_SIZE,
                        h_expand=True,
                        v_expand=True,
                    ),
                )
        except GLib.GError:
            # If the image is not available, use the symbolic icon
            logger.warning(f"{Colors.WARNING}[Notification] Image not available.")

        body_container.add(
            Label(
                markup=helpers.parse_markup(self._notification.body),
                v_align="start",
                h_expand=True,
                h_align="start",
                style="font-size: 13.5px;",
                line_wrap="word-char",
                chars_width=20,
                max_chars_width=40,
            ),
        )

        # Add the header, body, and actions to the notification box
        self.notification_box.children = (
            header_container,
            body_container,
        )

        # Add the notification box to the EventBox
        self.add(self.revealer)

        bulk_connect(
            self,
            {
                "enter-notify-event": lambda *_: self.notification_box.set_style(
                    "border: 1px solid #585b70;"
                ),
                "leave-notify-event": lambda *_: self.notification_box.set_style(
                    "border:none;"
                ),
            },
        )

        # Handle notification signals
        self._notification.connect("closed", self.on_notification_closed)

    def on_notification_closed(self, notification, reason):
        """Handle notification being closed."""
        if reason in ["dismissed-by-user", "dismissed-by-limit"]:
            self.revealer.set_reveal_child(False)
            GLib.timeout_add(400, self.destroy)

    def clear_notification(self, *_):
        notification_service.remove_notification(self._id)
        self.revealer.set_reveal_child(False)
        GLib.timeout_add(400, self.destroy)


class DateNotificationMenu(Box):
    """A menu to display the weather information."""

    def __init__(
        self,
        config,
        **kwargs,
    ):
        super().__init__(
            name="date-menu",
            orientation="h",
            **kwargs,
        )

        self.config = config

        self.clock_label = Label(
            label=time.strftime("%H:%M")
            if self.config["clock_format"] == "24h"
            else time.strftime("%I:%M"),
            style_classes="clock",
        )

        self.notifications: List[Notification] = notification_service.get_deserialized()

        self.notifications_list = [
            DateMenuNotification(notification=val, id=val["id"])
            for val in self.notifications
        ]

        self.notification_list_box = Box(
            orientation="v",
            h_align="center",
            spacing=8,
            h_expand=True,
            style_classes="notification-list",
            visible=len(self.notifications) > 0,
            children=self.notifications_list,
        )

        self.uptime = Label(style_classes="uptime", visible=config["uptime"])

        # Placeholder for when there are no notifications
        self.placeholder = Box(
            style_classes="placeholder",
            orientation="v",
            h_align="center",
            v_align="center",
            v_expand=True,
            h_expand=True,
            visible=len(self.notifications) == 0,  # visible if no notifications
            children=(
                Image(
                    icon_name=icons["notifications"]["silent"],
                    icon_size=64,
                ),
                Label(label="Your inbox is empty"),
            ),
        )

        # Header for the notification column
        self.dnd_switch = Gtk.Switch(
            name="notification-switch",
            active=False,
            valign=Gtk.Align.CENTER,
            visible=True,
        )

        notification_column_header = Box(
            style_classes="header",
            orientation="h",
            children=(Label(label="Do Not Disturb", name="dnd-text"), self.dnd_switch),
        )

        self.clear_icon = Image(
            icon_name=icons["trash"]["empty"]
            if len(self.notifications) == 0
            else icons["trash"]["full"],
            icon_size=13,
            name="clear-icon",
        )

        self.clear_button = HoverButton(
            name="clear-button",
            v_align="center",
            child=Box(
                children=(
                    Label(label="Clear"),
                    self.clear_icon,
                )
            ),
        )

        def handle_clear_click(*_):
            """Handle clear button click."""
            for child in self.notification_list_box.children:
                self.notification_list_box.remove(child)
                child.destroy()

            notification_service.clear_all_notifications()
            self.clear_icon.set_from_icon_name(icons["trash"]["empty"], 15)

        self.clear_button.connect(
            "clicked",
            handle_clear_click,
        )

        notification_column_header.pack_end(
            self.clear_button,
            False,
            False,
            0,
        )

        # Notification body column
        notification_column = Box(
            name="notification-column",
            orientation="v",
            visible=False,
            children=(
                notification_column_header,
                ScrolledWindow(
                    v_expand=True,
                    style_classes="notification-scrollable",
                    v_scrollbar_policy="automatic",
                    h_scrollbar_policy="never",
                    child=Box(children=(self.placeholder, self.notification_list_box)),
                ),
            ),
        )

        # Date and time column

        date_column = Box(
            style_classes="date-column",
            orientation="v",
            visible=False,
            children=(
                Box(
                    style_classes="clock-box",
                    orientation="v",
                    children=(self.clock_label, self.uptime),
                ),
                Box(
                    style_classes="calendar",
                    v_expand=True,
                    children=(
                        Gtk.Calendar(
                            visible=True,
                            hexpand=True,
                            halign=Gtk.Align.CENTER,
                        )
                    ),
                ),
            ),
        )

        self.children = (
            notification_column,
            Separator(),
            date_column,
        )

        if config["notification"]:
            notification_column.set_visible(True)

        if config["calendar"]:
            date_column.set_visible(True)

        bulk_connect(
            notification_service,
            {
                "notification-added": self.on_new_notification,
                "notification-closed": self.on_notification_closed,
                "clear_all": self.on_clear_all_notifications,
                "dnd": self.on_dnd_switch,
            },
        )

        self.dnd_switch.connect("notify::active", self.on_dnd_switch)

        # reusing the fabricator to call specified intervals
        util_fabricator.connect("changed", self.update_ui)

    def on_dnd_switch(self, _, value, *args):
        self.dnd_switch.set_active(value)

    def on_clear_all_notifications(self, *_):
        """Handle clearing all notifications."""
        self.clear_icon.set_from_icon_name(icons["trash"]["empty"], 15)

    def on_notification_closed(self, _, id, reason):
        """Handle notification being closed."""

        for child in self.notification_list_box.children:
            is_target = (
                isinstance(child, DateMenuNotification)
                and child._notification["id"] == id
            )
            if is_target:
                if reason in ["dismissed-by-user", "dismissed-by-limit"]:
                    child.revealer.set_reveal_child(False)
                    GLib.timeout_add(400, lambda: self._remove_notification(child))
                break

    def _remove_notification(self, widget):
        if widget in self.notification_list_box.children:
            self.notification_list_box.remove(widget)
            widget.destroy()
        return False

    def on_new_notification(self, fabric_notification, id):
        if notification_service.dont_disturb:
            return

        fabric_notification: Notification = (
            fabric_notification.get_notification_from_id(id)
        )

        # Clean up any destroyed widgets first
        try:
            active_children = [
                child
                for child in self.notification_list_box.children
                if child.get_parent() is not None
            ]
        except GLib.Error:
            logger.debug("[DateMenu] Error checking widget validity")
            active_children = []

        self.notification_list_box.children = active_children

        self.clear_icon.set_from_icon_name(icons["trash"]["full"], 15)

        self.notification_list_box.add(
            DateMenuNotification(
                notification=fabric_notification,
                id=id,
            )
        )
        self.placeholder.set_visible(False)
        self.notification_list_box.set_visible(True)

    def update_ui(self, fabricator, value):
        self.clock_label.set_text(
            time.strftime("%H:%M")
            if self.config["clock_format"] == "24h"
            else time.strftime("%I:%M"),
        )
        self.uptime.set_text(f"uptime: {uptime()}")
        return True


class DateTimeWidget(ButtonWidget):
    """A widget to power off the system."""

    def __init__(self, widget_config: BarConfig, **kwargs):
        super().__init__(widget_config["date_time"], name="datetime_menu", **kwargs)

        popup = Popover(
            content_factory=lambda: DateNotificationMenu(config=self.config),
            point_to=self,
        )
        self.notification_indicator = Image(
            icon_name=icons["notifications"]["noisy"],
            icon_size=14,
            visible=self.config["notification"]["enabled"],
        )

        self.count_label = Label(
            name="notification-count",
            label=str(notification_service.count),
            v_align="start",
            visible=self.config["notification"]["enabled"]
            and self.config["notification"]["count"],
        )

        if (
            self.config["notification"]["hide_count_on_zero"]
            and notification_service.count == 0
        ):
            self.count_label.set_visible(False)

        self.notification_indicator_box = Box(
            children=(self.notification_indicator, self.count_label)
        )

        self.connect(
            "clicked",
            popup.open,
        )

        self.children = Box(
            spacing=10,
            v_align="center",
            children=(
                self.notification_indicator_box,
                Separator(),
                DateTime(self.config["format"], name="date-time"),
            ),
        )

        bulk_connect(
            notification_service,
            {
                "notification_count": lambda _,
                value,
                *args: self.on_notification_count(value),
                "dnd": lambda _, value, *args: self.on_dnd_switch(value),
            },
        )

    def on_notification_count(self, value):
        if value > 0:
            self.count_label.set_text(str(value))
            self.count_label.set_visible(str(value))
        else:
            self.count_label.set_visible(False)

    def on_dnd_switch(self, value):
        if value:
            self.notification_indicator.set_from_icon_name(
                icons["notifications"]["silent"], icon_size=16
            )

        else:
            self.notification_indicator.set_from_icon_name(
                icons["notifications"]["noisy"], icon_size=16
            )
