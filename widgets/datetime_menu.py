import time
from typing import List

import gi
from fabric.notifications import Notification
from fabric.utils import bulk_connect, invoke_repeater
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
from services import NotificationCacheService, notification_service
from shared.custom_image import CustomImage
from shared.pop_over import PopOverWindow
from shared.separator import Separator
from shared.widget_container import ButtonWidget
from utils.colors import Colors
from utils.functions import uptime
from utils.icons import icons
from utils.widget_settings import BarConfig
from utils.widget_utils import get_icon, setup_cursor_hover

gi.require_version("Gtk", "3.0")


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
            name="notification-eventbox",
            pass_through=True,
            **kwargs,
        )

        self._notification = notification

        self._timeout_id = None

        self.cache_notification_service = NotificationCacheService().get_initial()

        self.notification_box = Box(
            spacing=8,
            name="notification",
            h_expand=True,
            orientation="v",
            style="border: none;",
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
                ellipsization="end",
                style_classes="summary",
                style="font-size: 13.5px;",
            ),
        )
        self.close_button = Button(
            style_classes="close-button",
            visible=True,
            image=Image(
                name="close-icon",
                icon_name=helpers.check_icon_exists(
                    "close-symbolic",
                    icons["ui"]["close"],
                ),
                icon_size=16,
            ),
            on_clicked=lambda _: self.clear_notification(id),
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
                    CustomImage(
                        pixbuf=image_pixbuf.scale_simple(
                            constants.NOTIFICATION_IMAGE_SIZE,
                            constants.NOTIFICATION_IMAGE_SIZE,
                            GdkPixbuf.InterpType.BILINEAR,
                        ),
                        style_classes="image",
                    ),
                )
        except GLib.GError:
            # If the image is not available, use the symbolic icon
            logger.warning(f"{Colors.WARNING}[Notification] Image not available.")

        body_container.add(
            Label(
                markup=helpers.parse_markup(self._notification.body),
                line_wrap="word-char",
                ellipsization="end",
                v_align="start",
                h_expand=True,
                h_align="start",
                style="font-size: 13.5px;",
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

    def clear_notification(self, id):
        self.cache_notification_service.remove_notification(id)
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

        self.cache_notification_service = NotificationCacheService().get_initial()

        self.clock_label = Label(
            label=time.strftime("%H:%M"),
            style_classes="clock",
        )

        self.notifications: List[Notification] = (
            self.cache_notification_service.get_deserialized()
        )

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

        self.uptime = Label(style_classes="uptime")

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

        notif_header = Box(
            style_classes="header",
            orientation="h",
            children=(Label(label="Do Not Disturb", name="dnd-text"), self.dnd_switch),
        )

        clear_button = Button(
            name="clear-button",
            v_align="center",
            child=Box(
                children=(
                    Label(label="Clear"),
                    Image(
                        icon_name=icons["trash"]["empty"]
                        if len(self.notifications) == 0
                        else icons["trash"]["full"],
                        icon_size=13,
                        name="clear-icon",
                    ),
                )
            ),
        )

        clear_button.connect(
            "clicked",
            lambda _: self.cache_notification_service.clear_all_notifications(),
        )

        setup_cursor_hover(clear_button)

        notif_header.pack_end(
            clear_button,
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
                notif_header,
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

        invoke_repeater(1000, self.update_labels, initial_call=True)
        notification_service.connect("notification-added", self.on_new_notification)
        self.cache_notification_service.connect(
            "clear_all", self.on_clear_all_notifications
        )

    def on_clear_all_notifications(self, *_):
        self.notification_list_box.children = []
        self.notifications = []
        self.notification_list_box.set_visible(False)
        self.placeholder.set_visible(True)

    def on_new_notification(self, fabric_notif, id):
        if self.cache_notification_service.dont_disturb:
            return

        notification: Notification = fabric_notif.get_notification_from_id(id)

        count = len(self.notification_list_box.children)

        self.notification_list_box.add(
            DateMenuNotification(
                notification=notification,
                id=count + 1 if count > 0 else 1,
            )
        )
        self.placeholder.set_visible(False)
        self.notification_list_box.set_visible(True)

    def update_labels(self):
        self.clock_label.set_text(time.strftime("%H:%M"))
        self.uptime.set_text(f"uptime: {uptime()}")
        return True


class DateTimeWidget(ButtonWidget):
    """A widget to power off the system."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(name="date-time-button", **kwargs)

        self.config = widget_config["date_time"]

        date_menu = DateNotificationMenu(config=self.config)

        popup = PopOverWindow(
            parent=bar,
            name="date-menu-popover",
            child=date_menu,
            visible=False,
            all_visible=False,
        )

        popup.set_pointing_to(self)

        self.notof_indicator = Image(
            icon_name=icons["notifications"]["noisy"],
            icon_size=16,
            visible=self.config["notification"],
        )

        count_label = Label(
            label=str(self.cache_notification_service.count),
            style_classes="notification-count",
            v_align="start",
            visible=self.config["notification_count"] and self.config["notification"],
        )

        self.notification_indicator_box = Box(
            children=(self.notof_indicator, count_label)
        )

        self.connect(
            "clicked",
            lambda *_: popup.set_visible(not popup.get_visible()),
        )

        self.children = Box(
            spacing=10,
            v_align="center",
            children=(
                self.notification_indicator_box,
                DateTime(self.config["format"], name="date-time"),
            ),
        )
        date_menu.dnd_switch.connect("notify::active", self.on_dnd_switch)

        bulk_connect(
            self.cache_notification_service,
            {
                "notification_count": lambda _, value, *args: count_label.set_text(
                    str(value)
                ),
            },
        )

    def on_dnd_switch(self, switch, _):
        """Handle the do not disturb switch."""
        if switch.get_active():
            self.notof_indicator.set_from_icon_name(
                icons["notifications"]["silent"], icon_size=16
            )
            self.cache_notification_service.dont_disturb = True

        else:
            self.notof_indicator.set_from_icon_name(
                icons["notifications"]["noisy"], icon_size=16
            )
            self.cache_notification_service.dont_disturb = False
