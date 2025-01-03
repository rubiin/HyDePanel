import json
from typing import List

from fabric.core.service import Service
from fabric.notifications import Notification
from loguru import logger

from utils.colors import Colors
from utils.config import NOTIFICATION_CACHE_FILE


class NotificationCacheService(Service):
    """A service to manage the notifications."""

    instance = None

    @staticmethod
    def get_initial():
        if NotificationCacheService.instance is None:
            NotificationCacheService.instance = NotificationCacheService()

        return NotificationCacheService.instance

    @property
    def notifications(self) -> List[Notification]:
        """Return the notifications."""
        return self._notifications

    @property
    def count(self) -> int:
        """Return the count of notifications."""
        return self._count

    @property
    def dont_disturb(self) -> bool:
        """Return the pause status."""
        return self._dont_disturb

    @dont_disturb.setter
    def dont_disturb(self, value: bool):
        """Set the pause status."""
        self._dont_disturb = value

    def __init__(self):
        self.do_read_notifications()
        self._dont_disturb = False

    def do_read_notifications(self) -> List[Notification]:
        """Read the notifications from the notifications file."""
        try:
            with open(NOTIFICATION_CACHE_FILE, "r") as file:
                notifications = json.load(file)
                self._notifications = [Notification.deserialize(data) for data in notifications]

                print(self._notifications)
                self._count = len(self._notifications)
        except FileNotFoundError:
            return []

    def cache_notification(self, data: Notification):
        """Cache the notification."""

        # Append the new notification to the list

        self._notifications.append(data)


        print("length is",len(self._notifications))

        if len(self._notifications) > 4:
            self._notifications = self._notifications[1:]

        print(self._notifications)

        # Serialize the notifications
        serialized_data = [Notification.serialize(data) for data in self._notifications]

        # self.do_read_notifications()


        # Combine existing and new notifications
        self._notifications.extend(serialized_data)

        # Write the updated data back to the cache file
        with open(NOTIFICATION_CACHE_FILE, "w") as f:
            json.dump(serialized_data, f, indent=2)

        logger.info(f"{Colors.INFO}[Notification] Notification cached successfully.")

    def clear_notifications(self):
        """Clear the notifications."""
        self._notifications = []
        self._count = 0

        # Write the updated data back to the cache file
        with open(NOTIFICATION_CACHE_FILE, "w") as f:
            json.dump([], f, indent=2)

        logger.info(f"{Colors.INFO}[Notification] Notifications cleared successfully.")
