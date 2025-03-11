<p align="center"><img src="./assets/hydepanel.png" align="centre" width="100" height="130"/></p>
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-8-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
<h1 align="center"><img src="https://raw.githubusercontent.com/JaKooLit/Telegram-Animated-Emojis/refs/heads/main/Activity/Sparkles.webp"/ height=50> HyDePanel</h1>
<p align="center">
 <a href="https://github.com/rubiin/HyDePanel/blob/master/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/rubiin/HyDePanel"></a>
  <a href='http://makeapullrequest.com'><img alt='PRs Welcome' src='https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=shields'/></a>
  <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/rubiin/HyDePanel"/>
  <img alt="GitHub closed issues" src="https://img.shields.io/github/issues-closed/rubiin/HyDePanel"/>
  <img alt="discord" src="https://img.shields.io/discord/1200448076620501063" />
</p>

A semi-customizable bar written using the [Fabric Widget System](https://github.com/Fabric-Development/fabric).
The panel focuses on providing an all-in-one, fully integrated panel experience, where users don’t have to rely on separate, theme-less third-party tools to manage niche functions like bluetooth, notifications and notification panel,on screen display.

<h2><sub><img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Camera%20with%20Flash.png" alt="Camera with Flash" width="25" height="25" /></sub> Screenshots</h2>

<table align="center">
  <tr>
    <td colspan="4"><img src="assets/screenshots/main.png"></td>
  </tr>
    <tr>
    <td colspan="4"><img src="assets/screenshots/main2.png"></td>
  </tr>
  <tr>
    <td colspan="1"><img src="assets/screenshots/quick_settings.png"></td>
    <td colspan="1"><img src="assets/screenshots/noti.png"></td>
    <td colspan="1" align="center"><img src="assets/screenshots/logout.png"></td>
    <td colspan="1" align="center"><img src="assets/screenshots/weather.png"></td>
  </tr>
</table>

<table align="center">
  <tr>
    <td align="center"><sup>✨ sᴜᴘᴘᴏʀᴛ ᴛʜᴇ ᴘʀᴏᴊᴇᴄᴛ ✨</sup></td>
  </tr>
  <tr>
    <td align="center">
      <a href='https://ko-fi.com/rubiin' target='_blank'>
        <img style='border:0px;height:128px;'
             src='https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExc3N4NzlvZWs2Z2tsaGx4aHgwa3UzMWVpcmNwZTNraTM2NW84ZDlqbiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/PaF9a1MpqDzovyqVKj/giphy.gif'
             border='0' alt='Support me on Ko-fi!' />
      </a>
    </td>
  </tr>
</table>

---

## Prerequisites

- [JetBrains Nerd Font](https://www.nerdfonts.com)
- [python 3+](https://www.python.org/downloads/)

---

## **Installation**

### Required

Most of these are already installed on existing working machines

```sh
## network
networkmanager

## Sound
pipewire

## Bluetooth menu utilities
gnome-bluetooth-3.0 # aur
bluez
bluez-utils

## Compiler for sass/scss
dart-sass

## Brightness module for OSD
brightnessctl
```

## To open and execute commands in a terminal ex: updates, cava

kitty

### Optional

```sh

## To check for updates using the default pacman script in the updates module
pacman-contrib

## To display cava audio visualizer
cava

## To switch between power profiles in the battery module
power-profiles-daemon

## To record screen through recorder module
wf-recorder & slurp

## To activate Hyprland’s native blue light filter
hyprsunset

## To activate Hyprland’s native idle inhibitor
hypridle

## To use media module on quick settings
playerctl

```

- Clone this repository:

```sh
git clone https://github.com/rubiin/HyDePanel.git ~/.config/hydepanel
cd bar
```

- Run the following command to install the required packages for particular os, few of them are already installed if you have a working system:

## Installation

You can choose one of two installation methods: **Automated Setup** or **Manual Setup**.

### Option 1: Automated Setup Using `init.sh -install`

1.  **Run the `init.sh -install` script** to automatically install all the required packages and dependencies (both `pacman` and AUR packages):

```sh
./init.sh -install
```

This script will:

- Install all required `pacman` and AUR packages.
- Set up the virtual environment and any required configurations.

1.  **Start the environment or bar** once the installation is complete:

```sh
./init.sh -start
```

This will launch the environment or bar as defined in your project.

### Option 2: Manual Setup (Install Dependencies First)

If you prefer to have more control over the installation process, you can install the required dependencies manually and then run the `init.sh -start` script.

#### Step 1: Install `pacman` Packages

Run the following command to install the required system packages:

```sh
	sudo pacman -S --noconfirm --needed pipewire playerctl dart-sass power-profiles-daemon networkmanager brightnessctl pkgconf wf-recorder kitty python pacman-contrib gtk3 cairo gtk-layer-shell libgirepository gobject-introspection gobject-introspection-runtime python-pip python-gobject python-psutil python-dbus python-cairo python-loguru python-setproctitle
```

#### Step 2: Install AUR Packages

Using `yay` to install the required AUR packages:

```sh
yay -S --needed gray-git python-fabric gnome-bluetooth-3.0 python-rlottie-python python-pytomlpp slurp imagemagick tesseract tesseract-data-eng
```

If you have something else besides `yay`, install with the respective aur helper.

#### Step 3: Run the `init.sh -start` Script

Once the dependencies are installed, run the following command to start the bar or environment:

```sh
./init.sh -start
```

## **Usage**

Add this to your `.config/hyprland.conf`

```sh
exec = `~/.config/hydepanel/init.sh -start`

```

> **Note**: modify the path accordingly

Check FAQs for common things you are likely to encounter

## Updating

Updating to latest commit is fairly simple, just git pull the latest changes.

> **Note**: make sure to keep the config safe just in case

## Check wiki for configuring individual widgets

## **Available Modules**

| **Item**              | **Description**                                                                |
| --------------------- | ------------------------------------------------------------------------------ |
| **battery**           | Widget that display battery status and usage information.                      |
| **bluetooth**         | Widget manages Bluetooth connections and settings.                             |
| **brightness**        | Widget controls the screen brightness level.                                   |
| **cava**              | An audio visualizer widget.                                                    |
| **click_counter**     | Widget tracks the number of mouse clicks.                                      |
| **cpu**               | Widget displays CPU usage and performance statistics.                          |
| **date_time**         | A menu displaying the current date and notifications.                          |
| **divider (utility)** | Widget separates sections in a user interface for better organization.         |
| **hypr_idle**         | Widget that tracks idle time or status of the system.                          |
| **hypr_picker**       | Widget that picks color from images.                                           |
| **hypr_sunset**       | Widget that adjusts screen settings based on the time of sunset.               |
| **keyboard**          | Widget that manages and manages the keyboard layout or settings.               |
| **language**          | Widget allows selection of the system's language or locale settings.           |
| **media**             | Widget controls media playback, volume, or other media-related settings.       |
| **microphone**        | Widget manages microphone settings and input levels.                           |
| **network_usage**     | Widget displays the upload/download speeds.                                    |
| **ocr**               | Widget scans text from an image.                                               |
| **power**             | Widget controls power-related settings, including sleep and shutdown.          |
| **ram**               | Widget displays information about system RAM usage and performance.            |
| **recorder**          | Widget for recording audio or video on the system.                             |
| **spacer (utility)**  | A simple utility for adding space in UI layouts.                               |
| **storage**           | Widget that displays storage usage and manages disk partitions or drives.      |
| **submap**            | Widget that displays active submap for hyprland.                               |
| **stop_watch**        | A utility for tracking elapsed time, like a timer or stopwatch.                |
| **system_tray**       | Widget that displays system tray icons and manages notifications.              |
| **taskbar**           | A bar at the bottom of the screen for quick access to apps and notifications.  |
| **updates**           | Widget that manages system updates, patches, and version upgrades.             |
| **quick_settings**    | Displays panel for quickly accessing some settings like brightness, sound etc. |
| **volume**            | Widget that controls the system’s audio volume.                                |
| **weather**           | Widget that displays current weather information or forecasts.                 |
| **window_title**      | Widget that shows the title of the current window or application.              |
| **workspaces**        | Widget that displays virtual desktops or workspaces.                           |

> [!WARNING]
> This is still in early development and will include breaking changes

## Frequently Asked Questions (FAQ)

### 1. **Cannot see system tray?**

Be sure to kill any bars that you may be running. You can kill other bar with `pkill bar-name`

### 2. **Cannot see notifications?**

Be sure to kill other notifications daemon that you may be running. You can kill other daemons with `pkill dunst; pkill mako;`

### 3. **Cannot see bar?**

Kill the app with `pkill hydepanel`. Run `init.sh -start`. This should show some logs. If it shows like `ModuleNotFoundError`, run `pip install -r requirements.txt`. If this does not solve the issue, do report a bug with screenshot of the log.

### 4. **No Blur?**

Add this to your `hyprland.conf`

```conf
layerrule = blur , fabric
layerrule = ignorezero, fabric
layerrule = blur ,gtk-layer-shell
layerrule = ignorezero ,gtk-layer-shell

```

## Contributing

We welcome all sorts of contributions, no matter how small, to this project! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute.

## Acknowledgements

- **Waybar** - A lot of the initial inspiration, and a pretty great bar.
  [Waybar GitHub Repository](https://github.com/Alexays/Waybar)

- **Hyprpanel** - Served as inspiration for some of the panel's features and design choices, with its focus on dynamic and customizable Hyprland panels.
  [Hyprpanel GitHub Repository](https://github.com/Jas-SinghFSU/HyprPanel)

## Special Thanks

A big thank you to the following people for their amazing help with code, bug fixes, and great ideas:

- [darsh](https://github.com/its-darsh): For creating fabric without which the project wouldn't have existed. Also, your quick feedbacks and problem-solving approach were a game-changer!
- [gummy bear album](https://github.com/muhchaudhary): For providing code snippets which served as a reference to start stuffs. Your creative ideas really pushed the project forward and made it better!
- [axenide](https://github.com/Axenide): For your fresh ideas and design references. Your code improvements and insights made a significant impact
- [sankalp](https://github.com/S4NKALP): For some bug fixes and recommendations,contributions in optimizing the code and identifying subtle bugs during the development period

# ⭐ Hit that Star Button!

Like what you see? Think this project is cooler than your morning coffee? ☕✨

Give it a star! It’s like giving a virtual high-five to the code—plus, and who doesn't love high-fives? ✋

Your star helps the project get noticed, and it makes us do a little happy dance. 💃

Just click the shiny "Star" button at the top right (it’s begging for your attention). 🥳

Thanks for making this project a little bit more awesome! 🚀

## Star History

<a href="https://star-history.com/#rubiin/HyDePanel&Timeline">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=rubiin/HyDePanel&type=Timeline&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=rubiin/HyDePanel&type=Timeline" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=rubiin/HyDePanel&type=Timeline" />
 </picture>
</a>

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/PixelKhaos"><img src="https://avatars.githubusercontent.com/u/5213174?v=4?s=100" width="100px;" alt="Robin Seger"/><br /><sub><b>Robin Seger</b></sub></a><br /><a href="https://github.com/rubiin/HyDePanel/commits?author=PixelKhaos" title="Code">💻</a> <a href="#design-PixelKhaos" title="Design">🎨</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://zaap.bio/Axenide"><img src="https://avatars.githubusercontent.com/u/66109459?v=4?s=100" width="100px;" alt="Adriano Tisera"/><br /><sub><b>Adriano Tisera</b></sub></a><br /><a href="https://github.com/rubiin/HyDePanel/commits?author=Axenide" title="Code">💻</a> <a href="https://github.com/rubiin/HyDePanel/issues?q=author%3AAxenide" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Anshul-007"><img src="https://avatars.githubusercontent.com/u/81582218?v=4?s=100" width="100px;" alt="Anshul J."/><br /><sub><b>Anshul J.</b></sub></a><br /><a href="https://github.com/rubiin/HyDePanel/commits?author=Anshul-007" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/S4NKALP"><img src="https://avatars.githubusercontent.com/u/98226895?v=4?s=100" width="100px;" alt="Sankalp Tharu"/><br /><sub><b>Sankalp Tharu</b></sub></a><br /><a href="https://github.com/rubiin/HyDePanel/issues?q=author%3AS4NKALP" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/keepo-dot"><img src="https://avatars.githubusercontent.com/u/201014163?v=4?s=100" width="100px;" alt="Keepo"/><br /><sub><b>Keepo</b></sub></a><br /><a href="https://github.com/rubiin/HyDePanel/commits?author=keepo-dot" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://evrenos-dev.vercel.app/"><img src="https://avatars.githubusercontent.com/u/138004078?v=4?s=100" width="100px;" alt="Sayeed Mahmood Evrenos"/><br /><sub><b>Sayeed Mahmood Evrenos</b></sub></a><br /><a href="https://github.com/rubiin/HyDePanel/issues?q=author%3AEvren-os" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://xeyossr.github.io"><img src="https://avatars.githubusercontent.com/u/113219171?v=4?s=100" width="100px;" alt="xeyossr"/><br /><sub><b>xeyossr</b></sub></a><br /><a href="https://github.com/rubiin/HyDePanel/commits?author=xeyossr" title="Documentation">📖</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://dimflix-official.github.io/"><img src="https://avatars.githubusercontent.com/u/112165977?v=4?s=100" width="100px;" alt="DIMFLIX"/><br /><sub><b>DIMFLIX</b></sub></a><br /><a href="https://github.com/rubiin/HyDePanel/issues?q=author%3ADIMFLIX-OFFICIAL" title="Bug reports">🐛</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
