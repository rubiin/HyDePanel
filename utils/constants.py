from gi.repository import GLib

# constants

NOTIFICATION_WIDTH = 400
NOTIFICATION_IMAGE_SIZE = 64
NOTIFICATION_ACTION_NUMBER = 3
HIGH_POLL_INTERVAL = 3600  # 1 hour in seconds

APPLICATION_NAME = "hydepanel"
SYSTEM_CACHE_DIR = GLib.get_user_cache_dir()
APP_CACHE_DIRECTORY = f"{SYSTEM_CACHE_DIR}/{APPLICATION_NAME}"


NOTIFICATION_CACHE_FILE = f"{APP_CACHE_DIRECTORY}/notifications.json"
WEATHER_CACHE_FILE = f"{APP_CACHE_DIRECTORY}/weather.json"


VALID_ANCHORS = [
    "top-left",
    "top-right",
    "top",
    "bottom-left",
    "bottom-right",
    "bottom",
    "left",
    "right",
    "center",
]

# Default configuration values
DEFAULT_CONFIG = {
    "$schema": "./hydepanel.schema.json",
    "battery": {
        "full_battery_level": 100,
        "hide_label_when_full": True,
        "label": True,
        "tooltip": True,
    },
    "quick_settings": {
        "media": {
            "ignore": [],
            "truncation_size": 26,
            "show_album": True,
            "show_artist": True,
            "show_time": True,
            "show_time_tooltip": True,
        },
        "shortcuts": [],  # Empty list by default - shortcuts are optional
    },
    "bluetooth": {
        "icon_size": 14,
        "label": True,
        "tooltip": True,
    },
    "brightness": {
        "icon_size": "14px",
        "label": True,
        "tooltip": True,
        "step_size": 5,
    },
    "cava": {"bars": 10, "color": "#89b4fa"},
    "overview": {},
    "click_counter": {"count": 0},
    "cpu": {
        "icon": "",
        "icon_size": "12px",
        "label": True,
        "tooltip": True,
        "round": True,
        "unit": "celsius",
        "show_unit": True,
        "sensor": "",
    },
    "date_time": {
        "format": "%b %d %H:%M",
        "notification_count": True,
        "calendar": True,
        "notification": True,
        "clock_format": "12h",
        "uptime": True,
    },
    "divider": {"size": 2},
    "hypr_idle": {
        "enabled_icon": "",
        "disabled_icon": "",
        "icon_size": "12px",
        "label": True,
        "tooltip": True,
    },
    "hypr_picker": {
        "icon": "",
        "icon_size": "14px",
        "tooltip": True,
        "label": True,
    },
    "hypr_sunset": {
        "temperature": "2800k",
        "enabled_icon": "󱩌",
        "disabled_icon": "󰛨",
        "icon_size": "12px",
        "label": True,
        "tooltip": True,
    },
    "keyboard": {
        "icon": "󰌌",
        "icon_size": "14px",
        "label": True,
        "tooltip": True,
    },
    "language": {
        "icon": "",
        "icon_size": "14px",
        "tooltip": True,
        "truncation_size": 2,
    },
    "module_groups": [
        {
            "widgets": ["updates", "battery"],
            "spacing": 4,
            "style_classes": ["bordered"],
        },
        {
            "widgets": ["quick_settings", "cpu"],
            "spacing": 0,
            "style_classes": ["compact"],
        },
    ],
    "layout": {
        "left_section": ["workspaces", "window_title"],
        "middle_section": ["date_time"],
        "right_section": ["@group:0", "@group:1", "system_tray"],
    },
    "memory": {
        "icon": "",
        "icon_size": "12px",
        "label": True,
        "tooltip": True,
    },
    "network_usage": {
        "icon_size": "14px",
        "upload_icon": "",
        "download_icon": "",
        "tooltip": True,
        "download": True,
        "upload": True,
    },
    "microphone": {
        "icon_size": "12px",
        "label": False,
        "tooltip": True,
    },
    "mpris": {
        "truncation_size": 30,
        "tooltip": True,
    },
    "notification": {
        "anchor": "top-right",
        "auto_dismiss": True,
        "ignored": [],
        "timeout": 3000,
        "max_count": 200,
        "per_app_limits": {},
        "play_sound": False,
        "sound_file": "notification4",
    },
    "osd": {
        "enabled": True,
        "timeout": 1500,
        "anchor": "bottom-center",
        "show_label": True,
        "show_percentage": True,
        "style": "default",
    },
    "ocr": {
        "icon": "󰐳",
        "icon_size": "14px",
        "tooltip": True,
        "label": True,
    },
    "general": {
        "screen_corners": {
            "enabled": False,
            "size": 20,
        },
        "desktop_clock": {
            "enabled": True,
            "anchor": "center",
            "date_format": "%A, %d %B %Y",
        },
        "check_updates": False,
        "layer": "top",
        "auto_hide": False,
        "debug": True,
        "bar_style": "default",
        "location": "top",
        "widget_style": "default",
    },
    "power": {
        "icon": "󰐥",
        "icon_size": "18px",
        "tooltip": True,
        "buttons": [
            "lock",
            "logout",
            "suspend",
            "hibernate",
            "shutdown",
            "reboot",
        ],
    },
    "recorder": {
        "path": "Videos/Screencasting",
        "icon_size": 16,
        "tooltip": True,
        "audio": True,
    },
    "spacing": {"size": 20},
    "stop_watch": {"stopped_icon": "󱫞", "running_icon": "󱫠", "icon_size": "16px"},
    "storage": {
        "icon": "󰋊",
        "icon_size": "14px",
        "label": True,
        "tooltip": True,
        "path": "/",
    },
    "submap": {
        "icon": "󰌌",
        "icon_size": "12px",
        "label": True,
        "tooltip": True,
    },
    "system_tray": {"icon_size": 16, "ignored": [], "hidden":[]},
    "task_bar": {"icon_size": 22},
    "theme": {
        "name": "catpuccin-mocha",
    },
    "theme_switcher": {
        "icon": "",
        "icon_size": "14px",
        "notify": False,  # Whether to show a notification when the theme is changed
    },
    "updates": {
        "os": "arch",
        "icon": "󱧘",
        "icon_size": "14px",
        "interval": HIGH_POLL_INTERVAL,
        "tooltip": True,
        "label": True,
    },
    "volume": {
        "icon_size": "14px",
        "label": True,
        "tooltip": True,
        "step_size": 5,
    },
    "weather": {
        "detect_location": False,
        "location": "kathmandu",
        "label": True,
        "tooltip": True,
        "interval": HIGH_POLL_INTERVAL,
    },
    "window_title": {
        "enable_icon": True,
        "truncation": True,
        "truncation_size": 50,
        "title_map": [],
    },
    "workspaces": {
        "count": 8,
        "hide_unoccupied": True,
        "ignored": [-99],
        "reverse_scroll": False,
        "empty_scroll": False,
        "default_label_format": "{id}",
        "icon_map": {"1": "1", "2": "2", "3": "3"},
    },
}

# sourced from hyprpanel
KBLAYOUT_MAP = {
    "Abkhazian (Russia)": "RU (Ab)",
    "Akan": "GH (Akan)",
    "Albanian": "AL",
    "Albanian (Plisi)": "AL (Plisi)",
    "Albanian (Veqilharxhi)": "AL (Veqilharxhi)",
    "Amharic": "ET",
    "Arabic": "ARA",
    "Arabic (Algeria)": "DZ (Ar)",
    "Arabic (AZERTY, Eastern Arabic numerals)": "ARA (Azerty Digits)",
    "Arabic (AZERTY)": "ARA (Azerty)",
    "Arabic (Buckwalter)": "ARA (Buckwalter)",
    "Arabic (Eastern Arabic numerals)": "ARA (Digits)",
    "Arabic (Macintosh)": "ARA (Mac)",
    "Arabic (Morocco)": "MA",
    "Arabic (OLPC)": "ARA (Olpc)",
    "Arabic (Pakistan)": "PK (Ara)",
    "Arabic (QWERTY, Eastern Arabic numerals)": "ARA (Qwerty Digits)",
    "Arabic (QWERTY)": "ARA (Qwerty)",
    "Arabic (Syria)": "SY",
    "Armenian": "AM",
    "Armenian (alt. eastern)": "AM (Eastern-Alt)",
    "Armenian (alt. phonetic)": "AM (Phonetic-Alt)",
    "Armenian (eastern)": "AM (Eastern)",
    "Armenian (phonetic)": "AM (Phonetic)",
    "Armenian (western)": "AM (Western)",
    "Asturian (Spain, with bottom-dot H and L)": "ES (Ast)",
    "Avatime": "GH (Avn)",
    "Azerbaijani": "AZ",
    "Azerbaijani (Cyrillic)": "AZ (Cyrillic)",
    "Azerbaijani (Iran)": "IR (Azb)",
    "Bambara": "ML",
    "Bangla": "BD",
    "Bangla (India, Baishakhi InScript)": "IN (Ben Inscript)",
    "Bangla (India, Baishakhi)": "IN (Ben Baishakhi)",
    "Bangla (India, Bornona)": "IN (Ben Bornona)",
    "Bangla (India, Gitanjali)": "IN (Ben Gitanjali)",
    "Bangla (India, Probhat)": "IN (Ben Probhat)",
    "Bangla (India)": "IN (Ben)",
    "Bangla (Probhat)": "BD (Probhat)",
    "Bashkirian": "RU (Bak)",
    "Belarusian": "BY",
    "Belarusian (intl.)": "BY (Intl)",
    "Belarusian (Latin)": "BY (Latin)",
    "Belarusian (legacy)": "BY (Legacy)",
    "Belarusian (phonetic)": "BY (Phonetic)",
    "Belgian": "BE",
    "Belgian (alt.)": "BE (Oss)",
    "Belgian (ISO, alt.)": "BE (Iso-Alternate)",
    "Belgian (Latin-9 only, alt.)": "BE (Oss Latin9)",
    "Belgian (no dead keys)": "BE (Nodeadkeys)",
    "Belgian (Wang 724 AZERTY)": "BE (Wang)",
    "Berber (Algeria, Latin)": "DZ",
    "Berber (Algeria, Tifinagh)": "DZ (Ber)",
    "Berber (Morocco, Tifinagh alt.)": "MA (Tifinagh-Alt)",
    "Berber (Morocco, Tifinagh extended phonetic)": "MA (Tifinagh-Extended-Phonetic)",
    "Berber (Morocco, Tifinagh extended)": "MA (Tifinagh-Extended)",
    "Berber (Morocco, Tifinagh phonetic, alt.)": "MA (Tifinagh-Alt-Phonetic)",
    "Berber (Morocco, Tifinagh phonetic)": "MA (Tifinagh-Phonetic)",
    "Berber (Morocco, Tifinagh)": "MA (Tifinagh)",
    "Bosnian": "BA",
    "Bosnian (US, with Bosnian digraphs)": "BA (Unicodeus)",
    "Bosnian (US)": "BA (Us)",
    "Bosnian (with Bosnian digraphs)": "BA (Unicode)",
    "Bosnian (with guillemets)": "BA (Alternatequotes)",
    "Braille": "BRAI",
    "Braille (left-handed inverted thumb)": "BRAI (Left Hand Invert)",
    "Braille (left-handed)": "BRAI (Left Hand)",
    "Braille (right-handed inverted thumb)": "BRAI (Right Hand Invert)",
    "Braille (right-handed)": "BRAI (Right Hand)",
    "Breton (France)": "FR (Bre)",
    "Bulgarian": "BG",
    "Bulgarian (enhanced)": "BG (Bekl)",
    "Bulgarian (new phonetic)": "BG (Bas Phonetic)",
    "Bulgarian (traditional phonetic)": "BG (Phonetic)",
    "Burmese": "MM",
    "Burmese Zawgyi": "MM (Zawgyi)",
    "Cameroon (AZERTY, intl.)": "CM (Azerty)",
    "Cameroon (Dvorak, intl.)": "CM (Dvorak)",
    "Cameroon Multilingual (QWERTY, intl.)": "CM (Qwerty)",
    "Canadian (CSA)": "CA (Multix)",
    "Catalan (Spain, with middle-dot L)": "ES (Cat)",
    "Cherokee": "US (Chr)",
    "Chinese": "CN",
    "Chuvash": "RU (Cv)",
    "Chuvash (Latin)": "RU (Cv Latin)",
    "CloGaelach": "IE (CloGaelach)",
    "Crimean Tatar (Turkish Alt-Q)": "UA (Crh Alt)",
    "Crimean Tatar (Turkish F)": "UA (Crh F)",
    "Crimean Tatar (Turkish Q)": "UA (Crh)",
    "Croatian": "HR",
    "Croatian (US, with Croatian digraphs)": "HR (Unicodeus)",
    "Croatian (US)": "HR (Us)",
    "Croatian (with Croatian digraphs)": "HR (Unicode)",
    "Croatian (with guillemets)": "HR (Alternatequotes)",
    "Czech": "CZ",
    "Czech (QWERTY, extended backslash)": "CZ (Qwerty Bksl)",
    "Czech (QWERTY, Macintosh)": "CZ (Qwerty-Mac)",
    "Czech (QWERTY)": "CZ (Qwerty)",
    "Czech (UCW, only accented letters)": "CZ (Ucw)",
    "Czech (US, Dvorak, UCW support)": "CZ (Dvorak-Ucw)",
    "Czech (with <\\|> key)": "CZ (Bksl)",
    "Danish": "DK",
    "Danish (Dvorak)": "DK (Dvorak)",
    "Danish (Macintosh, no dead keys)": "DK (Mac Nodeadkeys)",
    "Danish (Macintosh)": "DK (Mac)",
    "Danish (no dead keys)": "DK (Nodeadkeys)",
    "Danish (Windows)": "DK (Winkeys)",
    "Dari": "AF",
    "Dari (Afghanistan, OLPC)": "AF (Fa-Olpc)",
    "Dhivehi": "MV",
    "Dutch": "NL",
    "Dutch (Macintosh)": "NL (Mac)",
    "Dutch (standard)": "NL (Std)",
    "Dutch (US)": "NL (Us)",
    "Dzongkha": "BT",
    "English (Australian)": "AU",
    "English (Cameroon)": "CM",
    "English (Canada)": "CA (Eng)",
    "English (classic Dvorak)": "US (Dvorak-Classic)",
    "English (Colemak-DH ISO)": "US (Colemak Dh Iso)",
    "English (Colemak-DH)": "US (Colemak Dh)",
    "English (Colemak)": "US (Colemak)",
    "English (Dvorak, alt. intl.)": "US (Dvorak-Alt-Intl)",
    "English (Dvorak, intl., with dead keys)": "US (Dvorak-Intl)",
    "English (Dvorak, left-handed)": "US (Dvorak-L)",
    "English (Dvorak, Macintosh)": "US (Dvorak-Mac)",
    "English (Dvorak, right-handed)": "US (Dvorak-R)",
    "English (Dvorak)": "US (Dvorak)",
    "English (Ghana, GILLBT)": "GH (Gillbt)",
    "English (Ghana, multilingual)": "GH (Generic)",
    "English (Ghana)": "GH",
    "English (India, with rupee)": "IN (Eng)",
    "English (intl., with AltGr dead keys)": "US (Altgr-Intl)",
    "English (Macintosh)": "US (Mac)",
    "English (Mali, US, intl.)": "ML (Us-Intl)",
    "English (Mali, US, Macintosh)": "ML (Us-Mac)",
    "English (Nigeria)": "NG",
    "English (Norman)": "US (Norman)",
    "English (programmer Dvorak)": "US (Dvp)",
    "English (South Africa)": "ZA",
    "English (the divide/multiply toggle the layout)": "US (Olpc2)",
    "English (UK, Colemak-DH)": "GB (Colemak Dh)",
    "English (UK, Colemak)": "GB (Colemak)",
    "English (UK, Dvorak, with UK punctuation)": "GB (Dvorakukp)",
    "English (UK, Dvorak)": "GB (Dvorak)",
    "English (UK, extended, Windows)": "GB (Extd)",
    "English (UK, intl., with dead keys)": "GB (Intl)",
    "English (UK, Macintosh, intl.)": "GB (Mac Intl)",
    "English (UK, Macintosh)": "GB (Mac)",
    "English (UK)": "GB",
    "English (US, alt. intl.)": "US (Alt-Intl)",
    "English (US, euro on 5)": "US (Euro)",
    "English (US, intl., with dead keys)": "US (Intl)",
    "English (US, Symbolic)": "US (Symbolic)",
    "English (US)": "US",
    "English (Workman, intl., with dead keys)": "US (Workman-Intl)",
    "English (Workman)": "US (Workman)",
    "Esperanto": "EPO",
    "Esperanto (Brazil, Nativo)": "BR (Nativo-Epo)",
    "Esperanto (legacy)": "EPO (Legacy)",
    "Esperanto (Portugal, Nativo)": "PT (Nativo-Epo)",
    "Estonian": "EE",
    "Estonian (Dvorak)": "EE (Dvorak)",
    "Estonian (no dead keys)": "EE (Nodeadkeys)",
    "Estonian (US)": "EE (Us)",
    "Ewe": "GH (Ewe)",
    "Faroese": "FO",
    "Faroese (no dead keys)": "FO (Nodeadkeys)",
    "Filipino": "PH",
    "Filipino (Capewell-Dvorak, Baybayin)": "PH (Capewell-Dvorak-Bay)",
    "Filipino (Capewell-Dvorak, Latin)": "PH (Capewell-Dvorak)",
    "Filipino (Capewell-QWERF 2006, Baybayin)": "PH (Capewell-Qwerf2k6-Bay)",
    "Filipino (Capewell-QWERF 2006, Latin)": "PH (Capewell-Qwerf2k6)",
    "Filipino (Colemak, Baybayin)": "PH (Colemak-Bay)",
    "Filipino (Colemak, Latin)": "PH (Colemak)",
    "Filipino (Dvorak, Baybayin)": "PH (Dvorak-Bay)",
    "Filipino (Dvorak, Latin)": "PH (Dvorak)",
    "Filipino (QWERTY, Baybayin)": "PH (Qwerty-Bay)",
    "Finnish": "FI",
    "Finnish (classic, no dead keys)": "FI (Nodeadkeys)",
    "Finnish (classic)": "FI (Classic)",
    "Finnish (Macintosh)": "FI (Mac)",
    "Finnish (Windows)": "FI (Winkeys)",
    "French": "FR",
    "French (alt., Latin-9 only)": "FR (Oss Latin9)",
    "French (alt., no dead keys)": "FR (Oss Nodeadkeys)",
    "French (alt.)": "FR (Oss)",
    "French (AZERTY, AFNOR)": "FR (Afnor)",
    "French (AZERTY)": "FR (Azerty)",
    "French (BEPO, AFNOR)": "FR (Bepo Afnor)",
    "French (BEPO, Latin-9 only)": "FR (Bepo Latin9)",
    "French (BEPO)": "FR (Bepo)",
    "French (Cameroon)": "CM (French)",
    "French (Canada, Dvorak)": "CA (Fr-Dvorak)",
    "French (Canada, legacy)": "CA (Fr-Legacy)",
    "French (Canada)": "CA",
    "French (Democratic Republic of the Congo)": "CD",
    "French (Dvorak)": "FR (Dvorak)",
    "French (legacy, alt., no dead keys)": "FR (Latin9 Nodeadkeys)",
    "French (legacy, alt.)": "FR (Latin9)",
    "French (Macintosh)": "FR (Mac)",
    "French (Mali, alt.)": "ML (Fr-Oss)",
    "French (Morocco)": "MA (French)",
    "French (no dead keys)": "FR (Nodeadkeys)",
    "French (Switzerland, Macintosh)": "CH (Fr Mac)",
    "French (Switzerland, no dead keys)": "CH (Fr Nodeadkeys)",
    "French (Switzerland)": "CH (Fr)",
    "French (Togo)": "TG",
    "French (US)": "FR (Us)",
    "Friulian (Italy)": "IT (Fur)",
    "Fula": "GH (Fula)",
    "Ga": "GH (Ga)",
    "Georgian": "GE",
    "Georgian (ergonomic)": "GE (Ergonomic)",
    "Georgian (France, AZERTY Tskapo)": "FR (Geo)",
    "Georgian (Italy)": "IT (Geo)",
    "Georgian (MESS)": "GE (Mess)",
    "German": "DE",
    "German (Austria, Macintosh)": "AT (Mac)",
    "German (Austria, no dead keys)": "AT (Nodeadkeys)",
    "German (Austria)": "AT",
    "German (dead acute)": "DE (Deadacute)",
    "German (dead grave acute)": "DE (Deadgraveacute)",
    "German (dead tilde)": "DE (Deadtilde)",
    "German (Dvorak)": "DE (Dvorak)",
    "German (E1)": "DE (E1)",
    "German (E2)": "DE (E2)",
    "German (Macintosh, no dead keys)": "DE (Mac Nodeadkeys)",
    "German (Macintosh)": "DE (Mac)",
    "German (Neo 2)": "DE (Neo)",
    "German (no dead keys)": "DE (Nodeadkeys)",
    "German (QWERTY)": "DE (Qwerty)",
    "German (Switzerland, legacy)": "CH (Legacy)",
    "German (Switzerland, Macintosh)": "CH (De Mac)",
    "German (Switzerland, no dead keys)": "CH (De Nodeadkeys)",
    "German (Switzerland)": "CH",
    "German (T3)": "DE (T3)",
    "German (US)": "DE (Us)",
    "Greek": "GR",
    "Greek (extended)": "GR (Extended)",
    "Greek (no dead keys)": "GR (Nodeadkeys)",
    "Greek (polytonic)": "GR (Polytonic)",
    "Greek (simple)": "GR (Simple)",
    "Gujarati": "IN (Guj)",
    "Hanyu Pinyin Letters (with AltGr dead keys)": "CN (Altgr-Pinyin)",
    "Hausa (Ghana)": "GH (Hausa)",
    "Hausa (Nigeria)": "NG (Hausa)",
    "Hawaiian": "US (Haw)",
    "Hebrew": "IL",
    "Hebrew (Biblical, Tiro)": "IL (Biblical)",
    "Hebrew (lyx)": "IL (Lyx)",
    "Hebrew (phonetic)": "IL (Phonetic)",
    "Hindi (Bolnagri)": "IN (Bolnagri)",
    "Hindi (KaGaPa, phonetic)": "IN (Hin-Kagapa)",
    "Hindi (Wx)": "IN (Hin-Wx)",
    "Hungarian": "HU",
    "Hungarian (no dead keys)": "HU (Nodeadkeys)",
    "Hungarian (QWERTY, 101-key, comma, dead keys)": "HU (101 Qwerty Comma Dead)",
    "Hungarian (QWERTY, 101-key, comma, no dead keys)": "HU (101 Qwerty Comma Nodead)",
    "Hungarian (QWERTY, 101-key, dot, dead keys)": "HU (101 Qwerty Dot Dead)",
    "Hungarian (QWERTY, 101-key, dot, no dead keys)": "HU (101 Qwerty Dot Nodead)",
    "Hungarian (QWERTY, 102-key, comma, dead keys)": "HU (102 Qwerty Comma Dead)",
    "Hungarian (QWERTY, 102-key, comma, no dead keys)": "HU (102 Qwerty Comma Nodead)",
    "Hungarian (QWERTY, 102-key, dot, dead keys)": "HU (102 Qwerty Dot Dead)",
    "Hungarian (QWERTY, 102-key, dot, no dead keys)": "HU (102 Qwerty Dot Nodead)",
    "Hungarian (QWERTY)": "HU (Qwerty)",
    "Hungarian (QWERTZ, 101-key, comma, dead keys)": "HU (101 Qwertz Comma Dead)",
    "Hungarian (QWERTZ, 101-key, comma, no dead keys)": "HU (101 Qwertz Comma Nodead)",
    "Hungarian (QWERTZ, 101-key, dot, dead keys)": "HU (101 Qwertz Dot Dead)",
    "Hungarian (QWERTZ, 101-key, dot, no dead keys)": "HU (101 Qwertz Dot Nodead)",
    "Hungarian (QWERTZ, 102-key, comma, dead keys)": "HU (102 Qwertz Comma Dead)",
    "Hungarian (QWERTZ, 102-key, comma, no dead keys)": "HU (102 Qwertz Comma Nodead)",
    "Hungarian (QWERTZ, 102-key, dot, dead keys)": "HU (102 Qwertz Dot Dead)",
    "Hungarian (QWERTZ, 102-key, dot, no dead keys)": "HU (102 Qwertz Dot Nodead)",
    "Hungarian (standard)": "HU (Standard)",
    "Icelandic": "IS",
    "Icelandic (Dvorak)": "IS (Dvorak)",
    "Icelandic (Macintosh, legacy)": "IS (Mac Legacy)",
    "Icelandic (Macintosh)": "IS (Mac)",
    "Igbo": "NG (Igbo)",
    "Indian": "IN",
    "Indic IPA": "IN (Iipa)",
    "Indonesian (Arab Melayu, extended phonetic)": "ID (Melayu-Phoneticx)",
    "Indonesian (Arab Melayu, phonetic)": "ID (Melayu-Phonetic)",
    "Indonesian (Arab Pegon, phonetic)": "ID (Pegon-Phonetic)",
    "Indonesian (Latin)": "ID",
    "Inuktitut": "CA (Ike)",
    "Iraqi": "IQ",
    "Irish": "IE",
    "Irish (UnicodeExpert)": "IE (UnicodeExpert)",
    "Italian": "IT",
    "Italian (IBM 142)": "IT (Ibm)",
    "Italian (intl., with dead keys)": "IT (Intl)",
    "Italian (Macintosh)": "IT (Mac)",
    "Italian (no dead keys)": "IT (Nodeadkeys)",
    "Italian (US)": "IT (Us)",
    "Italian (Windows)": "IT (Winkeys)",
    "Japanese": "JP",
    "Japanese (Dvorak)": "JP (Dvorak)",
    "Japanese (Kana 86)": "JP (Kana86)",
    "Japanese (Kana)": "JP (Kana)",
    "Japanese (Macintosh)": "JP (Mac)",
    "Japanese (OADG 109A)": "JP (OADG109A)",
    "Javanese": "ID (Javanese)",
    "Kabyle (AZERTY, with dead keys)": "DZ (Azerty-Deadkeys)",
    "Kabyle (QWERTY, UK, with dead keys)": "DZ (Qwerty-Gb-Deadkeys)",
    "Kabyle (QWERTY, US, with dead keys)": "DZ (Qwerty-Us-Deadkeys)",
    "Kalmyk": "RU (Xal)",
    "Kannada": "IN (Kan)",
    "Kannada (KaGaPa, phonetic)": "IN (Kan-Kagapa)",
    "Kashubian": "PL (Csb)",
    "Kazakh": "KZ",
    "Kazakh (extended)": "KZ (Ext)",
    "Kazakh (Latin)": "KZ (Latin)",
    "Kazakh (with Russian)": "KZ (Kazrus)",
    "Khmer (Cambodia)": "KH",
    "Kikuyu": "KE (Kik)",
    "Komi": "RU (Kom)",
    "Korean": "KR",
    "Korean (101/104-key compatible)": "KR (Kr104)",
    "Kurdish (Iran, Arabic-Latin)": "IR (Ku Ara)",
    "Kurdish (Iran, F)": "IR (Ku F)",
    "Kurdish (Iran, Latin Alt-Q)": "IR (Ku Alt)",
    "Kurdish (Iran, Latin Q)": "IR (Ku)",
    "Kurdish (Iraq, Arabic-Latin)": "IQ (Ku Ara)",
    "Kurdish (Iraq, F)": "IQ (Ku F)",
    "Kurdish (Iraq, Latin Alt-Q)": "IQ (Ku Alt)",
    "Kurdish (Iraq, Latin Q)": "IQ (Ku)",
    "Kurdish (Syria, F)": "SY (Ku F)",
    "Kurdish (Syria, Latin Alt-Q)": "SY (Ku Alt)",
    "Kurdish (Syria, Latin Q)": "SY (Ku)",
    "Kurdish (Turkey, F)": "TR (Ku F)",
    "Kurdish (Turkey, Latin Alt-Q)": "TR (Ku Alt)",
    "Kurdish (Turkey, Latin Q)": "TR (Ku)",
    "Kyrgyz": "KG",
    "Kyrgyz (phonetic)": "KG (Phonetic)",
    "Lao": "LA",
    "Lao (STEA)": "LA (Stea)",
    "Latvian": "LV",
    "Latvian (adapted)": "LV (Adapted)",
    "Latvian (apostrophe)": "LV (Apostrophe)",
    "Latvian (ergonomic)": "LV (Ergonomic)",
    "Latvian (F)": "LV (Fkey)",
    "Latvian (modern)": "LV (Modern)",
    "Latvian (tilde)": "LV (Tilde)",
    "Lithuanian": "LT",
    "Lithuanian (IBM LST 1205-92)": "LT (Ibm)",
    "Lithuanian (LEKP)": "LT (Lekp)",
    "Lithuanian (LEKPa)": "LT (Lekpa)",
    "Lithuanian (Ratise)": "LT (Ratise)",
    "Lithuanian (standard)": "LT (Std)",
    "Lithuanian (US)": "LT (Us)",
    "Lower Sorbian": "DE (Dsb)",
    "Lower Sorbian (QWERTZ)": "DE (Dsb Qwertz)",
    "Macedonian": "MK",
    "Macedonian (no dead keys)": "MK (Nodeadkeys)",
    "Malay (Jawi, Arabic Keyboard)": "MY",
    "Malay (Jawi, phonetic)": "MY (Phonetic)",
    "Malayalam": "IN (Mal)",
    "Malayalam (enhanced InScript, with rupee)": "IN (Mal Enhanced)",
    "Malayalam (Lalitha)": "IN (Mal Lalitha)",
    "Maltese": "MT",
    "Maltese (UK, with AltGr overrides)": "MT (Alt-Gb)",
    "Maltese (US, with AltGr overrides)": "MT (Alt-Us)",
    "Maltese (US)": "MT (Us)",
    "Manipuri (Eeyek)": "IN (Eeyek)",
    "Maori": "MAO",
    "Marathi (enhanced InScript)": "IN (Marathi)",
    "Marathi (KaGaPa, phonetic)": "IN (Mar-Kagapa)",
    "Mari": "RU (Chm)",
    "Mmuock": "CM (Mmuock)",
    "Moldavian": "MD",
    "Moldavian (Gagauz)": "MD (Gag)",
    "Mon": "MM (Mnw)",
    "Mon (A1)": "MM (Mnw-A1)",
    "Mongolian": "MN",
    "Mongolian (Bichig)": "CN (Mon Trad)",
    "Mongolian (Galik)": "CN (Mon Trad Galik)",
    "Mongolian (Manchu Galik)": "CN (Mon Manchu Galik)",
    "Mongolian (Manchu)": "CN (Mon Trad Manchu)",
    "Mongolian (Todo Galik)": "CN (Mon Todo Galik)",
    "Mongolian (Todo)": "CN (Mon Trad Todo)",
    "Mongolian (Xibe)": "CN (Mon Trad Xibe)",
    "Montenegrin": "ME",
    "Montenegrin (Cyrillic, with guillemets)": "ME (Cyrillicalternatequotes)",
    "Montenegrin (Cyrillic, ZE and ZHE swapped)": "ME (Cyrillicyz)",
    "Montenegrin (Cyrillic)": "ME (Cyrillic)",
    "Montenegrin (Latin, QWERTY)": "ME (Latinyz)",
    "Montenegrin (Latin, Unicode, QWERTY)": "ME (Latinunicodeyz)",
    "Montenegrin (Latin, Unicode)": "ME (Latinunicode)",
    "Montenegrin (Latin, with guillemets)": "ME (Latinalternatequotes)",
    "N'Ko (AZERTY)": "GN",
    "Nepali": "NP",
    "Northern Saami (Finland)": "FI (Smi)",
    "Northern Saami (Norway, no dead keys)": "NO (Smi Nodeadkeys)",
    "Northern Saami (Norway)": "NO (Smi)",
    "Northern Saami (Sweden)": "SE (Smi)",
    "Norwegian": "NO",
    "Norwegian (Colemak)": "NO (Colemak)",
    "Norwegian (Dvorak)": "NO (Dvorak)",
    "Norwegian (Macintosh, no dead keys)": "NO (Mac Nodeadkeys)",
    "Norwegian (Macintosh)": "NO (Mac)",
    "Norwegian (no dead keys)": "NO (Nodeadkeys)",
    "Norwegian (Windows)": "NO (Winkeys)",
    "Occitan": "FR (Oci)",
    "Ogham": "IE (Ogam)",
    "Ogham (IS434)": "IE (Ogam Is434)",
    "Ol Chiki": "IN (Olck)",
    "Old Turkic": "TR (Otk)",
    "Old Turkic (F)": "TR (Otkf)",
    "Oriya": "IN (Ori)",
    "Oriya (Bolnagri)": "IN (Ori-Bolnagri)",
    "Oriya (Wx)": "IN (Ori-Wx)",
    "Ossetian (Georgia)": "GE (Os)",
    "Ossetian (legacy)": "RU (Os Legacy)",
    "Ossetian (Windows)": "RU (Os Winkeys)",
    "Ottoman (F)": "TR (Otf)",
    "Ottoman (Q)": "TR (Ot)",
    "Pannonian Rusyn": "RS (Rue)",
    "Pashto": "AF (Ps)",
    "Pashto (Afghanistan, OLPC)": "AF (Ps-Olpc)",
    "Persian": "IR",
    "Persian (with Persian keypad)": "IR (Pes Keypad)",
    "Polish": "PL",
    "Polish (British keyboard)": "GB (Pl)",
    "Polish (Dvorak, with Polish quotes on key 1)": "PL (Dvorak Altquotes)",
    "Polish (Dvorak, with Polish quotes on quotemark key)": "PL (Dvorak Quotes)",
    "Polish (Dvorak)": "PL (Dvorak)",
    "Polish (legacy)": "PL (Legacy)",
    "Polish (programmer Dvorak)": "PL (Dvp)",
    "Polish (QWERTZ)": "PL (Qwertz)",
    "Portuguese": "PT",
    "Portuguese (Brazil, Dvorak)": "BR (Dvorak)",
    "Portuguese (Brazil, IBM/Lenovo ThinkPad)": "BR (Thinkpad)",
    "Portuguese (Brazil, Nativo for US keyboards)": "BR (Nativo-Us)",
    "Portuguese (Brazil, Nativo)": "BR (Nativo)",
    "Portuguese (Brazil, no dead keys)": "BR (Nodeadkeys)",
    "Portuguese (Brazil)": "BR",
    "Portuguese (Macintosh, no dead keys)": "PT (Mac Nodeadkeys)",
    "Portuguese (Macintosh)": "PT (Mac)",
    "Portuguese (Nativo for US keyboards)": "PT (Nativo-Us)",
    "Portuguese (Nativo)": "PT (Nativo)",
    "Portuguese (no dead keys)": "PT (Nodeadkeys)",
    "Punjabi (Gurmukhi Jhelum)": "IN (Jhelum)",
    "Punjabi (Gurmukhi)": "IN (Guru)",
    "Romanian": "RO",
    "Romanian (Germany, no dead keys)": "DE (Ro Nodeadkeys)",
    "Romanian (Germany)": "DE (Ro)",
    "Romanian (standard)": "RO (Std)",
    "Romanian (Windows)": "RO (Winkeys)",
    "Russian": "RU",
    "Russian (Belarus)": "BY (Ru)",
    "Russian (Czech, phonetic)": "CZ (Rus)",
    "Russian (DOS)": "RU (Dos)",
    "Russian (engineering, EN)": "RU (Ruchey En)",
    "Russian (engineering, RU)": "RU (Ruchey Ru)",
    "Russian (Georgia)": "GE (Ru)",
    "Russian (Germany, phonetic)": "DE (Ru)",
    "Russian (Kazakhstan, with Kazakh)": "KZ (Ruskaz)",
    "Russian (legacy)": "RU (Legacy)",
    "Russian (Macintosh)": "RU (Mac)",
    "Russian (phonetic, AZERTY)": "RU (Phonetic Azerty)",
    "Russian (phonetic, Dvorak)": "RU (Phonetic Dvorak)",
    "Russian (phonetic, French)": "RU (Phonetic Fr)",
    "Russian (phonetic, Windows)": "RU (Phonetic Winkeys)",
    "Russian (phonetic, YAZHERTY)": "RU (Phonetic YAZHERTY)",
    "Russian (phonetic)": "RU (Phonetic)",
    "Russian (Poland, phonetic Dvorak)": "PL (Ru Phonetic Dvorak)",
    "Russian (Sweden, phonetic, no dead keys)": "SE (Rus Nodeadkeys)",
    "Russian (Sweden, phonetic)": "SE (Rus)",
    "Russian (typewriter, legacy)": "RU (Typewriter-Legacy)",
    "Russian (typewriter)": "RU (Typewriter)",
    "Russian (Ukraine, standard RSTU)": "UA (Rstu Ru)",
    "Russian (US, phonetic)": "US (Rus)",
    "Saisiyat (Taiwan)": "TW (Saisiyat)",
    "Samogitian": "LT (Sgs)",
    "Sanskrit (KaGaPa, phonetic)": "IN (San-Kagapa)",
    "Scottish Gaelic": "GB (Gla)",
    "Serbian": "RS",
    "Serbian (Cyrillic, with guillemets)": "RS (Alternatequotes)",
    "Serbian (Cyrillic, ZE and ZHE swapped)": "RS (Yz)",
    "Serbian (Latin, QWERTY)": "RS (Latinyz)",
    "Serbian (Latin, Unicode, QWERTY)": "RS (Latinunicodeyz)",
    "Serbian (Latin, Unicode)": "RS (Latinunicode)",
    "Serbian (Latin, with guillemets)": "RS (Latinalternatequotes)",
    "Serbian (Latin)": "RS (Latin)",
    "Serbian (Russia)": "RU (Srp)",
    "Serbo-Croatian (US)": "US (Hbs)",
    "Shan": "MM (Shn)",
    "Shan (Zawgyi Tai)": "MM (Zgt)",
    "Sicilian": "IT (Scn)",
    "Silesian": "PL (Szl)",
    "Sindhi": "PK (Snd)",
    "Sinhala (phonetic)": "LK",
    "Sinhala (US)": "LK (Us)",
    "Slovak": "SK",
    "Slovak (extended backslash)": "SK (Bksl)",
    "Slovak (QWERTY, extended backslash)": "SK (Qwerty Bksl)",
    "Slovak (QWERTY)": "SK (Qwerty)",
    "Slovenian": "SI",
    "Slovenian (US)": "SI (Us)",
    "Slovenian (with guillemets)": "SI (Alternatequotes)",
    "Spanish": "ES",
    "Spanish (dead tilde)": "ES (Deadtilde)",
    "Spanish (Dvorak)": "ES (Dvorak)",
    "Spanish (Latin American, Colemak)": "LATAM (Colemak)",
    "Spanish (Latin American, dead tilde)": "LATAM (Deadtilde)",
    "Spanish (Latin American, Dvorak)": "LATAM (Dvorak)",
    "Spanish (Latin American, no dead keys)": "LATAM (Nodeadkeys)",
    "Spanish (Latin American)": "LATAM",
    "Spanish (Macintosh)": "ES (Mac)",
    "Spanish (no dead keys)": "ES (Nodeadkeys)",
    "Spanish (Windows)": "ES (Winkeys)",
    "Swahili (Kenya)": "KE",
    "Swahili (Tanzania)": "TZ",
    "Swedish": "SE",
    "Swedish (Dvorak, intl.)": "SE (Us Dvorak)",
    "Swedish (Dvorak)": "SE (Dvorak)",
    "Swedish (Macintosh)": "SE (Mac)",
    "Swedish (no dead keys)": "SE (Nodeadkeys)",
    "Swedish (Svdvorak)": "SE (Svdvorak)",
    "Swedish (US)": "SE (Us)",
    "Swedish Sign Language": "SE (Swl)",
    "Syriac": "SY (Syc)",
    "Syriac (phonetic)": "SY (Syc Phonetic)",
    "Taiwanese": "TW",
    "Taiwanese (indigenous)": "TW (Indigenous)",
    "Tajik": "TJ",
    "Tajik (legacy)": "TJ (Legacy)",
    "Tamil (InScript, with Arabic numerals)": "IN (Tam)",
    "Tamil (InScript, with Tamil numerals)": "IN (Tam Tamilnumbers)",
    "Tamil (Sri Lanka, TamilNet '99, TAB encoding)": "LK (Tam TAB)",
    "Tamil (Sri Lanka, TamilNet '99)": "LK (Tam Unicode)",
    "Tamil (TamilNet '99 with Tamil numerals)": "IN (Tamilnet Tamilnumbers)",
    "Tamil (TamilNet '99, TAB encoding)": "IN (Tamilnet TAB)",
    "Tamil (TamilNet '99, TSCII encoding)": "IN (Tamilnet TSCII)",
    "Tamil (TamilNet '99)": "IN (Tamilnet)",
    "Tarifit": "MA (Rif)",
    "Tatar": "RU (Tt)",
    "Telugu": "IN (Tel)",
    "Telugu (KaGaPa, phonetic)": "IN (Tel-Kagapa)",
    "Telugu (Sarala)": "IN (Tel-Sarala)",
    "Thai": "TH",
    "Thai (Pattachote)": "TH (Pat)",
    "Thai (TIS-820.2538)": "TH (Tis)",
    "Tibetan": "CN (Tib)",
    "Tibetan (with ASCII numerals)": "CN (Tib Asciinum)",
    "Tswana": "BW",
    "Turkish": "TR",
    "Turkish (Alt-Q)": "TR (Alt)",
    "Turkish (E)": "TR (E)",
    "Turkish (F)": "TR (F)",
    "Turkish (Germany)": "DE (Tr)",
    "Turkish (intl., with dead keys)": "TR (Intl)",
    "Turkmen": "TM",
    "Turkmen (Alt-Q)": "TM (Alt)",
    "Udmurt": "RU (Udm)",
    "Ukrainian": "UA",
    "Ukrainian (homophonic)": "UA (Homophonic)",
    "Ukrainian (legacy)": "UA (Legacy)",
    "Ukrainian (macOS)": "UA (MacOS)",
    "Ukrainian (phonetic)": "UA (Phonetic)",
    "Ukrainian (standard RSTU)": "UA (Rstu)",
    "Ukrainian (typewriter)": "UA (Typewriter)",
    "Ukrainian (Windows)": "UA (Winkeys)",
    "Urdu (alt. phonetic)": "IN (Urd-Phonetic3)",
    "Urdu (Pakistan, CRULP)": "PK (Urd-Crulp)",
    "Urdu (Pakistan, NLA)": "PK (Urd-Nla)",
    "Urdu (Pakistan)": "PK",
    "Urdu (phonetic)": "IN (Urd-Phonetic)",
    "Urdu (Windows)": "IN (Urd-Winkeys)",
    "Uyghur": "CN (Ug)",
    "Uzbek": "UZ",
    "Uzbek (Afghanistan, OLPC)": "AF (Uz-Olpc)",
    "Uzbek (Afghanistan)": "AF (Uz)",
    "Uzbek (Latin)": "UZ (Latin)",
    "Vietnamese": "VN",
    "Vietnamese (France)": "VN (Fr)",
    "Vietnamese (US)": "VN (Us)",
    "Wolof": "SN",
    "Yakut": "RU (Sah)",
    "Yoruba": "NG (Yoruba)",
    "Unknown Layout": "Unknown",
}


WINDOW_TITLE_MAP = [
    # Original Entries
    ["firefox", "󰈹", "Firefox"],
    ["microsoft-edge", "󰇩", "Edge"],
    ["discord", "", "Discord"],
    ["vesktop", "", "Vesktop"],
    ["org.kde.dolphin", "", "Dolphin"],
    ["plex", "󰚺", "Plex"],
    ["steam", "", "Steam"],
    ["spotify", "󰓇", "Spotify"],
    ["spotube", "󰓇", "Spotify"],
    ["ristretto", "󰋩", "Ristretto"],
    ["obsidian", "󱓧", "Obsidian"],
    # Browsers
    ["google-chrome", "", "Google Chrome"],
    ["brave-browser", "󰖟", "Brave Browser"],
    ["chromium", "", "Chromium"],
    ["opera", "", "Opera"],
    ["vivaldi", "󰖟", "Vivaldi"],
    ["waterfox", "󰖟", "Waterfox"],
    ["zen", "󰖟", "Zen Browser"],
    ["thorium", "󰖟", "Thorium"],
    ["tor-browser", "", "Tor Browser"],
    ["floorp", "󰈹", "Floorp"],
    # Terminals
    ["gnome-terminal", "", "GNOME Terminal"],
    ["kitty", "󰄛", "Kitty Terminal"],
    ["konsole", "", "Konsole"],
    ["alacritty", "", "Alacritty"],
    ["wezterm", "", "Wezterm"],
    ["foot", "󰽒", "Foot Terminal"],
    ["tilix", "", "Tilix"],
    ["xterm", "", "XTerm"],
    ["urxvt", "", "URxvt"],
    ["st", "", "st Terminal"],
    ["com.mitchellh.ghostty", "󰊠", "Ghostty"],
    # Development Tools
    ["code", "󰨞", "Visual Studio Code"],
    ["vscode", "󰨞", "VS Code"],
    ["sublime-text", "", "Sublime Text"],
    ["atom", "", "Atom"],
    ["android-studio", "󰀴", "Android Studio"],
    ["intellij-idea", "", "IntelliJ IDEA"],
    ["pycharm", "󱃖", "PyCharm"],
    ["webstorm", "󱃖", "WebStorm"],
    ["phpstorm", "󱃖", "PhpStorm"],
    ["eclipse", "", "Eclipse"],
    ["netbeans", "", "NetBeans"],
    ["docker", "", "Docker"],
    ["vim", "", "Vim"],
    ["neovim", "", "Neovim"],
    ["neovide", "", "Neovide"],
    ["emacs", "", "Emacs"],
    # Communication Tools
    ["slack", "󰒱", "Slack"],
    ["telegram-desktop", "", "Telegram"],
    ["org.telegram.desktop", "", "Telegram"],
    ["whatsapp", "󰖣", "WhatsApp"],
    ["teams", "󰊻", "Microsoft Teams"],
    ["skype", "󰒯", "Skype"],
    ["thunderbird", "", "Thunderbird"],
    # File Managers
    ["nautilus", "󰝰", "Files (Nautilus)"],
    ["thunar", "󰝰", "Thunar"],
    ["pcmanfm", "󰝰", "PCManFM"],
    ["nemo", "󰝰", "Nemo"],
    ["ranger", "󰝰", "Ranger"],
    ["doublecmd", "󰝰", "Double Commander"],
    ["krusader", "󰝰", "Krusader"],
    # Media Players
    ["vlc", "󰕼", "VLC Media Player"],
    ["mpv", "", "MPV"],
    ["rhythmbox", "󰓃", "Rhythmbox"],
    # Graphics Tools
    ["gimp", "", "GIMP"],
    ["inkscape", "", "Inkscape"],
    ["krita", "", "Krita"],
    ["blender", "󰂫", "Blender"],
    # Video Editing
    ["kdenlive", "", "Kdenlive"],
    # Games and Gaming Platforms
    ["lutris", "󰺵", "Lutris"],
    ["heroic", "󰺵", "Heroic Games Launcher"],
    ["minecraft", "󰍳", "Minecraft"],
    ["csgo", "󰺵", "CS:GO"],
    ["dota2", "󰺵", "Dota 2"],
    # Office and Productivity
    ["evernote", "", "Evernote"],
    ["sioyek", "", "Sioyek"],
    # Cloud Services and Sync
    ["dropbox", "󰇣", "Dropbox"],
    # Desktop
    ["^$", "󰇄", "Desktop"],
]


# Updated set of named colors
named_colors = {
    "alice blue",
    "antique white",
    "aqua",
    "aquamarine",
    "azure",
    "beige",
    "bisque",
    "black",
    "blanched almond",
    "blue",
    "blue violet",
    "brown",
    "burlywood",
    "cadet blue",
    "chartreuse",
    "chocolate",
    "coral",
    "cornflower blue",
    "cornsilk",
    "crimson",
    "cyan",
    "dark blue",
    "dark cyan",
    "dark goldenrod",
    "dark gray",
    "dark green",
    "dark khaki",
    "dark magenta",
    "dark olive green",
    "dark orange",
    "dark orchid",
    "dark red",
    "dark salmon",
    "dark sea green",
    "dark slate blue",
    "dark slate gray",
    "dark turquoise",
    "dark violet",
    "deep pink",
    "deep sky blue",
    "dim gray",
    "dodger blue",
    "firebrick",
    "floral white",
    "forest green",
    "fuchsia",
    "gainsboro",
    "ghost white",
    "gold",
    "goldenrod",
    "gray",
    "green",
    "green yellow",
    "honeydew",
    "hot pink",
    "indian red",
    "indigo",
    "ivory",
    "khaki",
    "lavender",
    "lavender blush",
    "lawn green",
    "lemon chiffon",
    "light blue",
    "light coral",
    "light cyan",
    "light goldenrod yellow",
    "light green",
    "light grey",
    "light pink",
    "light salmon",
    "light sea green",
    "light sky blue",
    "light slate gray",
    "light steel blue",
    "light yellow",
    "lime",
    "lime green",
    "linen",
    "magenta",
    "maroon",
    "medium aquamarine",
    "medium blue",
    "medium orchid",
    "medium purple",
    "medium sea green",
    "medium slate blue",
    "medium spring green",
    "medium turquoise",
    "medium violet red",
    "midnight blue",
    "mint cream",
    "misty rose",
    "moccasin",
    "navajo white",
    "navy",
    "old lace",
    "olive",
    "olive drab",
    "orange",
    "orange red",
    "orchid",
    "pale goldenrod",
    "pale green",
    "pale turquoise",
    "pale violet red",
    "papaya whip",
    "peach puff",
    "peru",
    "pink",
    "plum",
    "powder blue",
    "purple",
    "red",
    "rosy brown",
    "royal blue",
    "saddle brown",
    "salmon",
    "sandy brown",
    "sea green",
    "seashell",
    "sienna",
    "silver",
    "sky blue",
    "slate blue",
    "slate gray",
    "snow",
    "spring green",
    "steel blue",
    "tan",
    "teal",
    "thistle",
    "tomato",
    "turquoise",
    "violet",
    "wheat",
    "white",
    "white smoke",
    "yellow",
    "yellow green",
}
