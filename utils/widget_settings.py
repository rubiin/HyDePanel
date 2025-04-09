from typing import Dict, List, Literal, TypedDict

from utils.types import Anchor, Layer

# Common configuration fields that will be reused
BaseConfig = TypedDict("BaseConfig", {"label": bool, "tooltip": bool})

# Layout configuration
Layout = TypedDict(
    "Layout", {"left": List[str], "middle": List[str], "right": List[str]}
)


# Power button configuration
PowerButton = TypedDict(
    "PowerButton",
    {
        "icon": str,
        "icon_size": int,
        "tooltip": bool,
        "items_per_row": int,
        "buttons": Dict[
            Dict[
                Literal["shutdown", "reboot", "hibernate", "suspend", "lock", "logout"],
                str,
            ],
            str,
        ],
    },
)

# HyprSunset configuration
HyprSunset = TypedDict(
    "HyprSunset",
    {
        **BaseConfig.__annotations__,
        "temperature": str,
        "enabled_icon": str,
        "disabled_icon": str,
        "sunrise": str,
        "sunset": str,
    },
)

# TaskBar configuration
TaskBar = TypedDict(
    "TaskBar", {"icon_size": int, "ignored": List[str], "tooltip": bool}
)

# SystemTray configuration
SystemTray = TypedDict(
    "SystemTray",
    {
        "icon_size": int,
        "ignored": List[str],
        "pinned": List[str],
        "hidden": List[str],
        "visible_count": int,
    },
)

# HyprIdle configuration
HyprIdle = TypedDict(
    "HyprIdle",
    {**BaseConfig.__annotations__, "enabled_icon": str, "disabled_icon": str},
)

# Battery configuration
Battery = TypedDict(
    "Battery",
    {
        "label": bool,
        "tooltip": bool,
        "orientation": str,
        "full_battery_level": int,
        "hide_label_when_full": bool,
        "icon_size": int,
    },
)

# Theme configuration
Theme = TypedDict("Theme", {"name": str})

# ClickCounter configuration
ClickCounter = TypedDict("ClickCounter", {"count": int})

# StopWatch configuration
StopWatch = TypedDict(
    "StopWatch",
    {
        "stopped_icon": str,
        "running_icon": str,
    },
)


DesktopClock = TypedDict(
    "DesktopClock",
    {
        "enabled": bool,
        "anchor": Anchor,
        "date_format": str,
    },
)


ScreenCorners = TypedDict(
    "ScreenCorners",
    {"enabled": bool, "size": int},
)


Dock = TypedDict(
    "Dock",
    {
        "enabled": bool,
        "icon_size": int,
        "pinned_apps": List[str],
        "ignored_apps": List[str],
        "layer": Layer,
        "anchor": Anchor,
    },
)


# Bar configuration
General = TypedDict(
    "General",
    {
        "screen_corners": ScreenCorners,
        "dock": Dock,
        "desktop_clock": DesktopClock,
        "check_updates": bool,
        "debug": bool,
        "location": str,
        "layer": Layer,
        "bar_style": Literal["default", "floating"],
    },
)

# Cpu configuration
Cpu = TypedDict(
    "Cpu",
    {
        **BaseConfig.__annotations__,
        "icon": str,
        "sensor": str,
        "unit": Literal["celsius", "fahrenheit"],
        "show_unit": bool,
        "round": bool,
    },
)

# Mpris configuration
Mpris = TypedDict("Mpris", {**BaseConfig.__annotations__, "truncation_size": int})

# Memory configuration
Memory = TypedDict("Memory", {**BaseConfig.__annotations__, "icon": str})

# Submap configuration
Submap = TypedDict("Submap", {**BaseConfig.__annotations__, "icon": str})


# Network configuration
NetworkUsage = TypedDict(
    "NetworkUsage",
    {
        **BaseConfig.__annotations__,
        "upload_icon": str,
        "download_icon": str,
        "download": bool,
        "upload": bool,
    },
)

# Storage configuration
Storage = TypedDict("Storage", {**BaseConfig.__annotations__, "icon": str, "path": str})

# Workspaces configuration
Workspaces = TypedDict(
    "Workspaces",
    {"count": int, "occupied": bool, "ignored": List[int], "icon_map": dict},
)

# WindowTitle configuration
WindowTitle = TypedDict(
    "WindowTitle",
    {
        "icon": bool,
        "truncation": bool,
        "truncation_size": int,
        "title_map": List[Dict[str, str]],
    },
)

# Updates configuration
Updates = TypedDict(
    "Updates",
    {
        **BaseConfig.__annotations__,
        "os": str,
        "icon": str,
        "interval": int,
    },
)


# Bluetooth configuration
BlueTooth = TypedDict("BlueTooth", {"label": bool, "tooltip": bool, "icon_size": int})

# Weather configuration
Weather = TypedDict(
    "Weather",
    {
        "location": str,
        "interval": int,
        "tooltip": bool,
        "label": bool,
    },
)

# Keyboard configuration
Keyboard = TypedDict("Keyboard", {**BaseConfig.__annotations__, "icon": str})

# MicroPhone configuration
MicroPhone = TypedDict("MicroPhone", {**BaseConfig.__annotations__})

# Cava configuration
Cava = TypedDict("Cava", {"bars": int, "color": str})

# Overview configuration
Overview = TypedDict("Overview", {})

# DateTimeMenu configuration
DateTimeMenu = TypedDict(
    "DateTimeMenu",
    {
        "format": str,
        "notification_count": bool,
        "calendar": bool,
        "notification": bool,
        "hover_reveal": bool,
        "auto_hide": bool,
        "auto_hide_timeout": int,
    },
)

# ThemeSwitcher configuration
ThemeSwitcher = TypedDict("ThemeSwitcher", {**BaseConfig.__annotations__, "icon": str})

# Hyprpicker configuration
HyprPicker = TypedDict("HyprPicker", {**BaseConfig.__annotations__, "icon": str})

# OCR configuration
OCR = TypedDict("OCR", {**BaseConfig.__annotations__, "icon": str})

# Media configuration
Media = TypedDict(
    "Media",
    {
        "ignore": List[str],
        "truncation_size": int,
        "show_active_only": bool,
        "truncation_size": int,
        "show_album": bool,
        "show_artist": bool,
        "show_time": bool,
        "show_time_tooltip": bool,
    },
)

# QuickSettings configuration
QuickSettings = TypedDict(
    "QuickSettings",
    {
        "media": Media,
        "hover_reveal": bool,
        "auto_hide": bool,
        "auto_hide_timeout": int,
        "shortcuts": List[str],
    },
)

# Spacing configuration
Spacing = TypedDict("Spacing", {"size": int})

# Divider configuration
Divider = TypedDict("Divider", {"size": int})

# Language configuration
Language = TypedDict(
    "Language", {**BaseConfig.__annotations__, "icon": str, "truncation_size": int}
)

# Volume configuration
Volume = TypedDict("Volume", {**BaseConfig.__annotations__, "step_size": int})

# Brightness configuration
Brightness = TypedDict("Brightness", {**BaseConfig.__annotations__, "step_size": int})


# Notification configuration
Notification = TypedDict(
    "Notification",
    {
        "enabled": bool,
        "ignored": List[str],
        "timeout": int,
        "anchor": Anchor,
        "auto_dismiss": bool,
        "play_sound": bool,
        "sound_file": str,
        "max_count": int,
        "max_actions": int,
        "display_actions_on_hover": bool,
        "per_app_limits": Dict[str, int],
    },
)

# Recording configuration
Recording = TypedDict("Recording", {"path": str, "icon_size": int, "tooltip": bool})


# OSD configuration
OSD = TypedDict(
    "Osd",
    {
        "enabled": bool,
        "timeout": int,
        "anchor": Anchor,
        "percentage": bool,
        "icon_size": int,
    },
)


class BarConfig(TypedDict):
    """Main configuration that includes all other configurations"""

    battery: Battery
    bluetooth: BlueTooth
    brightness: Brightness
    cava: Cava
    click_counter: ClickCounter
    cpu: Cpu
    date_time: DateTimeMenu
    divider: Divider
    hypr_idle: HyprIdle
    hypr_sunset: HyprSunset
    hypr_picker: HyprPicker
    keyboard: Keyboard
    language: Language
    layout: Layout
    memory: Memory
    microphone: MicroPhone
    mpris: Mpris
    network_usage: NetworkUsage
    notification: Notification
    general: General
    ocr: OCR
    osd: OSD
    overview: Overview
    power: PowerButton
    quick_settings: QuickSettings
    recorder: Recording
    spacing: Spacing
    stop_watch: StopWatch
    storage: Storage
    system_tray: SystemTray
    submap: Submap
    task_bar: TaskBar
    theme: Theme
    theme_switcher: ThemeSwitcher
    updates: Updates
    volume: Volume
    weather: Weather
    window_title: WindowTitle
    workspaces: Workspaces
