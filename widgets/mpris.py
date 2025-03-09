from fabric import Fabricator
from fabric.utils import bulk_connect, get_relative_path
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer
from loguru import logger

from services import MprisPlayer, MprisPlayerManager
from shared.widget_container import ButtonWidget
from utils.colors import Colors
from utils.icons import common_text_icons
from utils.widget_settings import BarConfig


class Mpris(ButtonWidget):
    """A widget to control the MPRIS."""

    def __init__(
        self,
        widget_config: BarConfig,
        bar,
        **kwargs,
    ):
        # Initialize the EventBox with specific name and style
        super().__init__(
            **kwargs,
        )
        self.config = widget_config["mpris"]

        self.player = None

        self.text_icon = Label(
            label=common_text_icons["playing"],
        )

        self.label = Label(
            v_align="center",
            h_align="center",
            style="color: #cdd6f4;margin-right: 10px",
        )

        script_path = get_relative_path("../assets/scripts/cava.sh")

        # Services
        self.mpris_manager = MprisPlayerManager()

        for player in self.mpris_manager.players:
            logger.info(
                f"{Colors.INFO}[PLAYER MANAGER] player found: "
                f"{player.get_property('player-name')}",
            )
            self.player = MprisPlayer(player)
            bulk_connect(
                self.player,
                {
                    "notify::metadata": self.get_current,
                    "notify::playback-status": self.get_playback_status,
                },
            )


        self.box = Box(
            children=[self.label,self.text_icon],
        ).build(
            lambda box, _: Fabricator(
                poll_from=f"bash -c '{script_path} 8'",
                stream=True,
                on_changed=lambda f, line: self.label.set_label(line),
            )
        )

        self.children = self.box

        # Connect the button press event to the play_pause method
        bulk_connect(
            self,
            {
                "button-press-event": lambda *_: self.play_pause(),
            },
        )

    def get_current(self, *_):
        print("new song")
        bar_label = self.player.title

        truncated_info = (
            bar_label
            if len(bar_label) < self.config["truncation_size"]
            else bar_label[:30]
        )

        if self.config["tooltip"]:
            self.set_tooltip_text(truncated_info)

    def get_playback_status(self, *_):
        # Get the current playback status and change the icon accordingly

        status = self.player.playback_status.lower()
        if status == "playing":

            self.text_icon.set_label(common_text_icons["paused"])
        elif status == "paused":

            self.text_icon.set_label(common_text_icons["playing"])
        else:
            self.box.children = [self.text_icon]

    def play_pause(self, *_):
        # Toggle play/pause using playerctl
        if self.player is not None:
            self.player.play_pause()
