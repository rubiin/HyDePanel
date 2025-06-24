from utils.colors import Colors


class ExecutableNotFoundError(ImportError):
    """Raised when an executable is not found."""

    def __init__(self, executable_name: str):
        super().__init__(
            f"{Colors.ERROR}Executable {Colors.UNDERLINE}{executable_name}{Colors.RESET} not found. Please install it using your package manager."  # noqa: E501
        )


class NetworkManagerNotFoundError(ImportError):
    """
    Raised when NetworkManager is not found.
    """

    def __init__(self, *args: object) -> None:
        super().__init__(
            "NetworkManager not found! To use the network service, install NetworkManager",  # noqa: E501
            *args,
        )


class PlayerctlImportError(ImportError):
    """An error to raise when playerctl is not installed."""

    def __init__(self, *args):
        super().__init__(
            "Playerctl is not installed, please install it first",
            *args,
        )


class DisplayNotFoundError(Exception):
    """
    Raised when the display is not found (e.g., a Wayland compositor is not running).
    """

    def __init__(self, *args: object) -> None:
        super().__init__(
            "Display not found! Ensure you are running a Wayland compositor", *args
        )
