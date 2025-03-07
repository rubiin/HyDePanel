Welcome to the HyDePanel wiki!

# System Configuration

This repository defines the configuration settings for a modular system, allowing users to customize the layout, icons, intervals, and various components. The configuration is written in Python and structured using typed dictionaries for strong typing.

## Default Configuration

The default configuration is stored in the `DEFAULT_CONFIG` dictionary. It includes default values for various sections, such as the layout of the bar, settings for battery, CPU, weather, and other system components.

# General Configuration

```json
    "general": {
        "screen_corners": {
            "enabled": false,
            "size": 20,
        },
        "desktop_clock": {
            "enabled": false,
            "anchor": "center",
            "date_format": "%A, %d %B %Y",
        },
        "check_updates": false,
        "debug": false,
        "layer": "top",
        "auto_hide": false,
        "bar_style": "default",
        "location": "top",
        "widget_style": "default",
        "desktop_clock": true,
    }

```

- **debug** (boolean):
  Enable or disable debug mode for the panel. When set to true, additional debugging output or features may be activated.

- **location** (string; enum: "top", "bottom"):
  Determines where the panel is positioned on the screen. It can either be at the top or the bottom.

- **bar_style** (string; enum: "default", "floating"):
  Selects the style of the panel bar. "default" provides a standard appearance, while "floating" gives it a floating look.

- **layer** (string; enum: "background", "bottom", "top", "overlay"):
  Specifies the stacking order or z-index of the panel, determining which layer it should be rendered on.

- **widget_style** (string; enum: "default", "wave1", "wave2", "flat", "shadow"):
  Sets a visual style for the widgets on the panel. Each option represents a predefined look.

- **screen_corners.enabled** (boolean):
  Determines whether the screen corner feature is enabled or disabled.

- **screen_corners.size** (integer):
  Defines the size of the screen corner feature when enabled.

- **desktop_clock.enabled** (boolean):
  Enables or disables the desktop clock.

- **desktop_clock.anchor** (string; enum: "left", "center", "right"):
  Sets the anchor position of the desktop clock on the screen.

- **desktop_clock.date_format** (string):
  Specifies the format of the date displayed on the desktop clock. Example: `%A, %d %B %Y`.

- **check_updates** (boolean):
  Determines whether the system should automatically check for updates.

- **auto_hide** (boolean):
  Defines whether the panel should automatically hide when not in use.

## Layout Configuration

The layout configuration defines the sections of the bar and the components displayed in each section:

```json
"layout": {
    "left_section": ["workspaces", "window_title"],
    "middle_section": ["date_time"],
    "right_section": [
        "weather",
        "updates",
        "battery",
        "bluetooth",
        "system_tray",
        "power",
    ],
}
```

- **layout.left_section** (array of strings):
  Specifies the elements to be displayed in the left section of the panel. The order in the array determines the sequence.

  - `"workspaces"`: Displays workspace-related information.
  - `"window_title"`: Shows the title of the currently focused window.

- **layout.middle_section** (array of strings):
  Specifies the elements to be displayed in the middle section of the panel. The order in the array determines the sequence.

  - `"date_time"`: Displays the current date and time.

- **layout.right_section** (array of strings):
  Specifies the elements to be displayed in the right section of the panel. The order in the array determines the sequence.

# Component Configurations

Each component, such as hypr_sunset, battery, cpu, memory, etc., has its own configuration with customizable options. Here's an example for the battery component:

```json
"hypr_sunset": {
    "temperature": "2800k",
    "enabled_icon": "󱩌",
    "disabled_icon": "󰛨",
    "icon_size": "12px",
    "interval": 2000,
    "label": true,
    "tooltip": true
}
```

Other components follow a similar structure, where each configuration defines things like icon_size, label, and tooltip.

## Battery

```json
"battery": {
    "label": true,
    "tooltip": true,
    "hide_label_when_full": true,
    "full_battery_level": 100,
}
```

- **label** (boolean):
  Determines whether a label should be displayed. When set to true, the label will be shown.

- **tooltip** (boolean):
  Enables or disables tooltips. When set to true, hovering over elements will display a tooltip with additional information.

- **hide_label_when_full** (boolean):
  Specifies whether the label should be hidden when the relevant item is at full capacity or status. When set to true, the label will be hidden if the item is full.

- **full_battery_level** (integer):
  Defines the battery level percentage at which the system is considered to be fully charged. The default is 100.

## Bluetooth

```json
"bluetooth": {
    "icon_size": 22,
    "label": true,
    "tooltip": true,
}
```

- **icon_size** (integer):
  Specifies the size of the icons. The value is in pixels, and in this case, the icon size is set to 22 pixels.

- **label** (boolean):
  Determines whether a label should be displayed. When set to true, the label will be shown.

- **tooltip** (boolean):
  Enables or disables tooltips. When set to true, hovering over elements will display a tooltip with additional information.

## Brightness

```json
"brightness": {
    "icon_size": "14px",
    "label": true,
    "tooltip": true,
    "icon": "󰏨",
    "step_size": 5,
}
```

- **icon_size** (string):
  Specifies the size of the icons. The value is defined in CSS units (e.g., pixels), and in this case, the icon size is set to `"14px"`.

- **label** (boolean):
  Determines whether a label should be displayed. When set to true, the label will be shown.

- **tooltip** (boolean):
  Enables or disables tooltips. When set to true, hovering over elements will display a tooltip with additional information.

- **icon** (string):
  Defines the icon to be displayed. In this case, the icon is represented by the Unicode character `"󰏨"`.

- **step_size** (integer):
  Specifies the step size for any actions that involve incrementing or changing values. In this case, the step size is set to `5`.

## cava

```json
"cava": {
    "bars": 10,
    "color": "#89b4fa"
}
```

- **bars** (integer):
  Specifies the number of bars to be displayed. In this case, the number of bars is set to `10`.

- **color** (string):
  Defines the color to be used. The color is represented in hexadecimal format, and in this case, the color is `"#89b4fa"`.

## CPU

```json
"cpu": {
    "icon": "",
    "icon_size": "12px",
    "label": true,
    "tooltip": true,
}
```

- icon: The icon used to display the module.
- icon_size: Size of the icon in px.
- label: Whether to show a label.
- tooltip: Whether to show a tooltip.
- round: Whether to round the temperature.
- unit: The unit of the temperature.
- show_unit: Whether to show the unit.
- sensor: The sensor to use for temperature.

## HyprIdle

```json
"hypr_idle": {
    "enabled_icon": "",
    "disabled_icon": "",
    "icon_size": "12px",
    "label": true,
    "tooltip": true,
}
```

- enabled_icon: The icon used when enabled.
- disabled_icon: The icon used when disabled.
- icon_size: Size of the icon.
- label: Whether to show a label.
- tooltip: Whether to show a tooltip.

## HyprSunset

```json
"hypr_sunset": {
    "temperature": "2800k",
    "enabled_icon": "󱩌",
    "disabled_icon": "󰛨",
    "icon_size": "12px",
    "label": true,
    "tooltip": true,
}
```

- temperature: Sets the color temperature.
- enabled_icon: The icon used when enabled.
- disabled_icon: The icon used when disabled.
- icon_size: Size of the icon.
- label: Whether to show a label.
- tooltip: Whether to show a tooltip.

## Hyprpicker

```json
"hypr_picker": {
    "icon": "",
    "icon_size": "14px",
    "label": true,
    "tooltip": true,
}
```

- icon: The icon used to display the module.
- icon_size: Size of the icon in px.
- label: Whether to show a label.
- tooltip: Whether to show a tooltip

## Language

```json
"language": {"length": 3}

```

- length - Sets the length of the language display.

## Memory

```json
"memory": {
    "icon": "",
    "icon_size": "12px",
    "label": true,
    "tooltip": true,
}
```

- icon: The icon used to display the module.
- icon_size: Size of the icon in px.
- label: Whether to show a label.
- tooltip: Whether to show a tooltip

## MPRIS

```json
"mpris": {
    "truncation_size": 30,
    "format": "{artist} - {title}",
}
```

Configures the media player information system (MPRIS) display settings.

- truncation_size: The length of the MPRIS display.
- format: The format of the MPRIS display.

## OCR

```json
"ocr": {
    "icon": "󰐳",
    "icon_size": "14px",
    "label": true,
    "tooltip": true,
}
```

- icon: The icon used to display the module.
- icon_size: Size of the icon in px.
- label: Whether to show a label.
- tooltip: Whether to show a tooltip

## Power Button

```json
"power": {"icon": "󰐥", "icon_size": "12px", "tooltip": true}

```

- icon: The icon used to display the module.
- icon_size: Size of the icon in px.
- tooltip: Whether to show a tooltip

## Recorder

```json
"recorder": {
    "videos": "Videos/Screencasting",
    "tooltip": true,
    "audio": true,
    "icon_size": 14
}

```

- videos: Path to the videos directory.
- audio: Whether to record video with audio.
- tooltip: Whether to show a tooltip
- icon_size: Size of the icon in number

## Submap

```json
"submap": {
    "icon": "󰋊",
    "icon_size": "14px",
    "label": true,
    "tooltip": true,
}
```

- icon: The icon used to display the module.
- icon_size: Size of the icon in px.
- label: Whether to show a label.
- tooltip: Whether to show a tooltip

## Storage

```json
"storage": {
    "icon": "󰋊",
    "icon_size": "14px",
    "label": true,
    "tooltip": true,
}
```

- icon: The icon used to display the module.
- icon_size: Size of the icon in px.
- label: Whether to show a label.
- tooltip: Whether to show a tooltip

## TaskBar and System Tray

```json
"task_bar": {"icon_size": 22, "ignored": ["firefox"]},
"system_tray": {"icon_size": 22, "ignored": ["firefox"]},
```

- icon_size - the size of the icon in number
- ignored - list of applications to ignore

## Updates

```json
"updates": {
    "os": "arch",
    "icon": "󱧘",
    "icon_size": "14px",
    "interval": 60000,
    "tooltip": true,
    "label": true,
}
```

- os: The os to fetch updates count for.
- icon: The icon used to display the module.
- icon_size: Size of the icon in px.
- interval: The update interval for update.
- label: Whether to show a label.
- tooltip: Whether to show a tooltip

## Volume

```json
"volume": {
    "icon_size": "14px",
    "label": true,
    "tooltip": true,
    "step_size": 5,
}
```

- icon_size: Size of the icon in px.
- label: Whether to show a label.
- tooltip: Whether to show a tooltip
- step_size: The volume step size.

## Weather

```json
"weather": {
    "location": "Kathmandu",
    "interval": 60000,
    "tooltip": true,
    "label": true,
    "detect_location": false,
}
```

- location: The location to display weather for.
- interval: The update interval for weather.
- label: Whether to show a label.
- tooltip: Whether to show a tooltip
- detect_location: Whether to detect the location automatically.

## Window Title

```json
"window_title": {
    "truncation": true,
    "truncation_size": 50,
    "enable_icon": true,
    "title_map": []
    }

```

- truncation: whether to limit the window title.
- truncation_size: Maximum length for the window title (requires truncation set to true).
- enable_icon: Whether to display the icon in the title bar.
- title_map: Map of window title to icon.

## Workspaces

```json
"workspaces": {
  "count": 8,
  "hide_unoccupied": true,
    "reverse_scroll": false,
    "empty_scroll": false,
    "icon_map": {
      "1":"",
      "2": "",
      "3": "",
      "4": "󰏆",
      "5": "",
      "6": "󰕼",
      "7": "󰏦",
      "8": "󰏧"
    },
    "ignored": [1]
    }
```

- count: Number of workspaces.
- hide_unoccupied: Indicates whether workspaces should show as occupied or not.
- reverse_scroll: Invert scroll direction
- empty_scroll: scroll to empty workspaces
- icon_map: map an icon to a workspace instead of number
- ignored: ignores workspaces from the widget
