import json
from io import BytesIO
from pathlib import Path
from tarfile import TarFile, TarInfo
from tarfile import open as taropen
from typing import Literal, TypeAlias
from unicodedata import normalize
from urllib.request import urlretrieve

from catppuccin.models import Color
from catppuccin.palette import PALETTE, Flavor
from jsonschema import validate

icon_theme_t: TypeAlias = Literal["dark", "light"]
json_t: TypeAlias = bool | dict[str, "json_t"] | str


THEME_SCHEMA_URL: str = "https://raw.githubusercontent.com/Chatterino/chatterino2/master/docs/ChatterinoTheme.schema.json"  # fmt: skip # noqa: E501


def main() -> None:
    theme_schema: str = retrieve_via_http(THEME_SCHEMA_URL)

    for flavor in PALETTE:
        for color in flavor.colors:
            if not color.accent:
                continue

            target: str = normalize("NFKD", f"{flavor.name}-{color.name}").encode("ascii", "ignore").decode()

            dist_dir: Path = Path("dist")
            dist_dir.mkdir(parents=True, exist_ok=True)

            archive_path: Path = dist_dir.joinpath(f"{target}.tar.gz")
            with taropen(archive_path, "w:gz") as archive:
                # https://github.com/Chatterino/chatterino2/blob/38a7ce695485e080f6e98e17c9b2a01bcbf17744/src/singletons/Paths.hpp#L20
                settings_path: TarInfo = TarInfo("Settings/settings.json")
                settings: json_t = generate_settings(flavor, color, target=target)
                write_json_to_tar(archive=archive, path=settings_path, tree=settings)

                icon_theme: icon_theme_t = "light" if flavor.dark else "dark"
                # https://github.com/Chatterino/chatterino2/blob/38a7ce695485e080f6e98e17c9b2a01bcbf17744/src/singletons/Paths.hpp#L41
                theme_path: TarInfo = TarInfo(f"Themes/{target}.json")
                theme: json_t = generate_theme(flavor, color, icon_theme=icon_theme)
                validate(instance=theme, schema=json.loads(theme_schema))
                write_json_to_tar(archive=archive, path=theme_path, tree=theme)


def retrieve_via_http(url: str) -> str:
    if not url.startswith(("http:", "https:")):
        raise ValueError("URL must start with 'http:' or 'https:'")

    location, _ = urlretrieve(url)
    with open(location) as response:
        return response.read()


def write_json_to_tar(archive: TarFile, path: TarInfo, tree: json_t) -> None:
    tree_data: bytes = json.dumps(tree, indent=2, sort_keys=True).encode()
    path.size = len(tree_data)
    archive.addfile(path, BytesIO(tree_data))


def generate_settings(flavor: Flavor, accent: Color, target: str) -> json_t:
    opacity_first_messagee: int = 0x3C
    opacity_hype_chat: int = 0x3C
    opacity_mention: int = 0x7F
    opacity_redeem_highlight: int = 0x3C
    opacity_self: int = 0xFF
    opacity_subscription: int = 0x64
    opacity_tread_reply: int = 0x3C

    return {
        "appearance": {
            "messages": {
                "lastMessageColor": accent.hex,
                "showLastMessageIndicator": True,
            },
            "theme": {
                "name": f"{target}.json",
            },
        },
        "highlighting": {
            "elevatedMessageHighlight": {
                "color": f"#{opacity_hype_chat:02x}{flavor.colors.yellow.hex.lstrip('#')}",
            },
            "firstMessageHighlightColor": f"#{opacity_first_messagee:02x}{flavor.colors.green.hex.lstrip('#')}",
            "redeemedHighlightColor": f"#{opacity_redeem_highlight:02x}{flavor.colors.teal.hex.lstrip('#')}",
            "selfHighlightColor": f"#{opacity_mention:02x}{flavor.colors.red.hex.lstrip('#')}",
            "selfMessageHighlight": {
                "color": f"#{opacity_self:02x}{accent.hex.lstrip('#')}",
            },
            "subHighlightColor": f"#{opacity_subscription:02x}{flavor.colors.mauve.hex.lstrip('#')}",
            "threadHighlightColor": f"#{opacity_tread_reply:02x}{flavor.colors.red.hex.lstrip('#')}",
        },
    }


def generate_theme(flavor: Flavor, accent: Color, icon_theme: icon_theme_t) -> json_t:
    opacity_drop_preview: int = 0x30
    opacity_drop_target: int = 0x00
    opacity_highlight_end: int = 0x00
    opacity_highlight_start: int = 0x6E
    opacity_logs: int = 0x99
    opacity_scrollbar: int = 0x00
    opacity_selection: int = 0x40

    tabs_generic: json_t = {
        "hover": flavor.colors.mantle.hex,
        "regular": flavor.colors.mantle.hex,
        "unfocused": flavor.colors.mantle.hex,
    }

    return {
        "$schema": THEME_SCHEMA_URL,
        "colors": {
            "accent": accent.hex,
            "messages": {
                "backgrounds": {
                    "alternate": flavor.colors.base.hex,
                    "regular": flavor.colors.mantle.hex,
                },
                "disabled": f"#{opacity_logs:02x}{flavor.colors.crust.hex.lstrip('#')}",
                "highlightAnimationEnd": f"#{opacity_highlight_end:02x}{flavor.colors.overlay2.hex.lstrip('#')}",
                "highlightAnimationStart": f"#{opacity_highlight_start:02x}{flavor.colors.overlay2.hex.lstrip('#')}",
                "selection": f"#{opacity_selection:02x}{flavor.colors.text.hex.lstrip('#')}",
                "textColors": {
                    "caret": flavor.colors.text.hex,
                    "chatPlaceholder": flavor.colors.subtext1.hex,
                    "link": accent.hex,
                    "regular": flavor.colors.text.hex,
                    "system": flavor.colors.subtext0.hex,
                },
            },
            "scrollbars": {
                "background": f"#{opacity_scrollbar:02x}{flavor.colors.crust.hex.lstrip('#')}",
                "thumb": flavor.colors.overlay1.hex,
                "thumbSelected": flavor.colors.overlay0.hex,
            },
            "splits": {
                "background": flavor.colors.crust.hex,
                "dropPreview": f"#{opacity_drop_preview:02x}{accent.hex.lstrip('#')}",
                "dropPreviewBorder": accent.hex,
                "dropTargetRect": f"#{opacity_drop_target:02x}{accent.hex.lstrip('#')}",
                "dropTargetRectBorder": f"#{opacity_drop_target:02x}{accent.hex.lstrip('#')}",
                "header": {
                    "background": flavor.colors.mantle.hex,
                    "border": flavor.colors.crust.hex,
                    "focusedBackground": flavor.colors.mantle.hex,
                    "focusedBorder": flavor.colors.crust.hex,
                    "focusedText": flavor.colors.text.hex,
                    "text": flavor.colors.text.hex,
                },
                "input": {
                    "background": flavor.colors.mantle.hex,
                    "text": accent.hex,
                },
                "messageSeperator": flavor.colors.surface0.hex,
                "resizeHandle": accent.hex,
                "resizeHandleBackground": accent.hex,
            },
            "tabs": {
                "dividerLine": accent.hex,
                "highlighted": {
                    "backgrounds": tabs_generic,
                    "line": {
                        "hover": flavor.colors.red.hex,
                        "regular": flavor.colors.red.hex,
                        "unfocused": flavor.colors.red.hex,
                    },
                    "text": flavor.colors.subtext1.hex,
                },
                "newMessage": {
                    "backgrounds": tabs_generic,
                    "line": tabs_generic,
                    "text": flavor.colors.text.hex,
                },
                "regular": {
                    "backgrounds": tabs_generic,
                    "line": tabs_generic,
                    "text": flavor.colors.subtext0.hex,
                },
                "selected": {
                    "backgrounds": {
                        "hover": flavor.colors.surface0.hex,
                        "regular": flavor.colors.surface0.hex,
                        "unfocused": flavor.colors.surface0.hex,
                    },
                    "line": {
                        "hover": accent.hex,
                        "regular": accent.hex,
                        "unfocused": accent.hex,
                    },
                    "text": flavor.colors.text.hex,
                },
            },
            "window": {
                "background": flavor.colors.crust.hex,
                "text": flavor.colors.subtext1.hex,
            },
        },
        "metadata": {
            "iconTheme": icon_theme,
        },
    }


if __name__ == "__main__":
    main()
