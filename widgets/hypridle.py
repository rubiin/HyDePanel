from shared.buttontoggle import CommandSwitcher


class HyprIdleWidget(CommandSwitcher):
    """A widget to control the hypridle command."""

    def __init__(self, config, **kwargs):
        # Store the configuration for hypridle
        self.config = config["hypr_idle"]

        # Set the command to hypridle
        self.command = "hypridle"

        super().__init__(
            command=self.command,
            enabled_icon=self.config["enabled_icon"],
            disabled_icon=self.config["disabled_icon"],
            enable_label=self.config["enable_label"],
            enable_tooltip=self.config["enable_tooltip"],
            name="hypridle",
            **kwargs,
        )
