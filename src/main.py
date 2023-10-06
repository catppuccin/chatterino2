import io
import json
from dataclasses import dataclass
from pathlib import Path
from tarfile import TarFile, TarInfo
from tarfile import open as taropen
from typing import Literal, TypeAlias
from urllib.request import urlretrieve

from catppuccin import Colour, Flavour  # type: ignore
from jsonschema import validate

icon_theme_t: TypeAlias = Literal["dark", "light"]
json_t: TypeAlias = bool | dict[str, "json_t"] | str


@dataclass(frozen=True, kw_only=True)
class NamedColour(object):
    colour: Colour
    name: str


@dataclass(frozen=True, kw_only=True)
class NamedFlavour(object):
    flavour: Flavour
    icon_theme: icon_theme_t
    name: str


THEME_URL: str = "https://raw.githubusercontent.com/Chatterino/chatterino2/master/docs/ChatterinoTheme.schema.json"


def main() -> None:
    theme_schema: str = retrieve_via_http(THEME_URL)

    flavours: list[NamedFlavour] = [
        NamedFlavour(flavour=Flavour.frappe(), icon_theme="light", name="frappe"),
        NamedFlavour(flavour=Flavour.latte(), icon_theme="dark", name="latte"),
        NamedFlavour(flavour=Flavour.macchiato(), icon_theme="light", name="macchiato"),
        NamedFlavour(flavour=Flavour.mocha(), icon_theme="light", name="mocha"),
    ]

    for flavour in flavours:
        accents: list[NamedColour] = [
            NamedColour(colour=flavour.flavour.blue, name="blue"),
            NamedColour(colour=flavour.flavour.flamingo, name="flamingo"),
            NamedColour(colour=flavour.flavour.green, name="green"),
            NamedColour(colour=flavour.flavour.lavender, name="lavender"),
            NamedColour(colour=flavour.flavour.maroon, name="maroon"),
            NamedColour(colour=flavour.flavour.mauve, name="mauve"),
            NamedColour(colour=flavour.flavour.peach, name="peach"),
            NamedColour(colour=flavour.flavour.pink, name="pink"),
            NamedColour(colour=flavour.flavour.red, name="red"),
            NamedColour(colour=flavour.flavour.rosewater, name="rosewater"),
            NamedColour(colour=flavour.flavour.sapphire, name="sapphire"),
            NamedColour(colour=flavour.flavour.sky, name="sky"),
            NamedColour(colour=flavour.flavour.teal, name="teal"),
            NamedColour(colour=flavour.flavour.yellow, name="yellow"),
        ]

        for accent in accents:
            target: str = f"{flavour.name}-{accent.name}"

            dist_dir: Path = Path("dist")
            dist_dir.mkdir(parents=True, exist_ok=True)

            archive_path: Path = dist_dir.joinpath(f"{target}.tar.gz")
            with taropen(archive_path, "w:gz") as archive:
                # https://github.com/Chatterino/chatterino2/blob/38a7ce695485e080f6e98e17c9b2a01bcbf17744/src/singletons/Paths.hpp#L20
                settings_path: TarInfo = TarInfo("Settings/settings.json")
                settings: json_t = generate_settings(
                    flavour=flavour.flavour,
                    accent=accent.colour,
                    target=target,
                )
                write_json_to_tar(archive=archive, path=settings_path, tree=settings)

                # https://github.com/Chatterino/chatterino2/blob/38a7ce695485e080f6e98e17c9b2a01bcbf17744/src/singletons/Paths.hpp#L41
                theme_path: TarInfo = TarInfo(f"Themes/{target}.json")
                theme: json_t = generate_theme(
                    flavour=flavour.flavour,
                    accent=accent.colour,
                    icon_theme=flavour.icon_theme,
                )
                validate(instance=theme, schema=json.loads(theme_schema))
                write_json_to_tar(archive=archive, path=theme_path, tree=theme)


def retrieve_via_http(url: str) -> str:
    if not url.startswith(("http:", "https:")):
        raise ValueError("URL must start with 'http:' or 'https:'")

    location, headers = urlretrieve(url)
    with open(location) as response:
        return response.read()


def write_json_to_tar(archive: TarFile, path: TarInfo, tree: json_t) -> None:
    tree_data: bytes = json.dumps(tree, indent=2, sort_keys=True).encode()
    path.size = len(tree_data)
    archive.addfile(path, io.BytesIO(tree_data))


def generate_settings(flavour: Flavour, accent: Colour, target: str) -> json_t:
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
                "lastMessageColor": f"#{accent.hex}",
                "showLastMessageIndicator": True,
            },
            "theme": {
                "name": f"{target}.json",
            },
        },
        "highlighting": {
            "elevatedMessageHighlight": {
                "color": f"#{opacity_hype_chat:02x}{flavour.yellow.hex}",
            },
            "firstMessageHighlightColor": f"#{opacity_first_messagee:02x}{flavour.green.hex}",
            "redeemedHighlightColor": f"#{opacity_redeem_highlight:02x}{flavour.teal.hex}",
            "selfHighlightColor": f"#{opacity_mention:02x}{flavour.flamingo.hex}",
            "selfMessageHighlight": {
                "color": f"#{opacity_self:02x}{accent.hex}",
            },
            "subHighlightColor": f"#{opacity_subscription:02x}{flavour.mauve.hex}",
            "threadHighlightColor": f"#{opacity_tread_reply:02x}{flavour.red.hex}",
        },
    }


def generate_theme(flavour: Flavour, accent: Colour, icon_theme: icon_theme_t) -> json_t:
    opacity_drop_preview: int = 0x30
    opacity_drop_target: int = 0x00
    opacity_highlight_end: int = 0x00
    opacity_highlight_start: int = 0x6E
    opacity_logs: int = 0x99
    opacity_scrollbar: int = 0x00
    opacity_selection: int = 0x40

    tabs_generic: json_t = {
        "hover": f"#{flavour.mantle.hex}",
        "regular": f"#{flavour.mantle.hex}",
        "unfocused": f"#{flavour.mantle.hex}",
    }

    return {
        "$schema": THEME_URL,
        "colors": {
            "accent": f"#{accent.hex}",
            "messages": {
                "backgrounds": {
                    "alternate": f"#{flavour.base.hex}",
                    "regular": f"#{flavour.mantle.hex}",
                },
                "disabled": f"#{opacity_logs:02x}{flavour.crust.hex}",
                "highlightAnimationEnd": f"#{opacity_highlight_end:02x}{flavour.overlay2.hex}",
                "highlightAnimationStart": f"#{opacity_highlight_start:02x}{flavour.overlay2.hex}",
                "selection": f"#{opacity_selection:02x}{flavour.text.hex}",
                "textColors": {
                    "caret": f"#{flavour.text.hex}",
                    "chatPlaceholder": f"#{flavour.subtext1.hex}",
                    "link": f"#{accent.hex}",
                    "regular": f"#{flavour.text.hex}",
                    "system": f"#{flavour.subtext0.hex}",
                },
            },
            "scrollbars": {
                "background": f"#{opacity_scrollbar:02x}{flavour.crust.hex}",
                "thumb": f"#{flavour.overlay1.hex}",
                "thumbSelected": f"#{flavour.overlay0.hex}",
            },
            "splits": {
                "background": f"#{flavour.crust.hex}",
                "dropPreview": f"#{opacity_drop_preview:02x}{accent.hex}",
                "dropPreviewBorder": f"#{accent.hex}",
                "dropTargetRect": f"#{opacity_drop_target:02x}{accent.hex}",
                "dropTargetRectBorder": f"#{opacity_drop_target:02x}{accent.hex}",
                "header": {
                    "background": f"#{flavour.mantle.hex}",
                    "border": f"#{flavour.crust.hex}",
                    "focusedBackground": f"#{flavour.mantle.hex}",
                    "focusedBorder": f"#{flavour.crust.hex}",
                    "focusedText": f"#{flavour.text.hex}",
                    "text": f"#{flavour.text.hex}",
                },
                "input": {
                    "background": f"#{flavour.mantle.hex}",
                    "text": f"#{accent.hex}",
                },
                "messageSeperator": f"#{flavour.surface0.hex}",
                "resizeHandle": f"#{accent.hex}",
                "resizeHandleBackground": f"#{accent.hex}",
            },
            "tabs": {
                "dividerLine": f"#{accent.hex}",
                "highlighted": {
                    "backgrounds": tabs_generic,
                    "line": {
                        "hover": f"#{flavour.red.hex}",
                        "regular": f"#{flavour.red.hex}",
                        "unfocused": f"#{flavour.red.hex}",
                    },
                    "text": f"#{flavour.subtext1.hex}",
                },
                "newMessage": {
                    "backgrounds": tabs_generic,
                    "line": tabs_generic,
                    "text": f"#{flavour.text.hex}",
                },
                "regular": {
                    "backgrounds": tabs_generic,
                    "line": tabs_generic,
                    "text": f"#{flavour.subtext0.hex}",
                },
                "selected": {
                    "backgrounds": {
                        "hover": f"#{flavour.surface0.hex}",
                        "regular": f"#{flavour.surface0.hex}",
                        "unfocused": f"#{flavour.surface0.hex}",
                    },
                    "line": {
                        "hover": f"#{accent.hex}",
                        "regular": f"#{accent.hex}",
                        "unfocused": f"#{accent.hex}",
                    },
                    "text": f"#{flavour.text.hex}",
                },
            },
            "window": {
                "background": f"#{flavour.crust.hex}",
                "text": f"#{flavour.subtext1.hex}",
            },
        },
        "metadata": {
            "iconTheme": icon_theme,
        },
    }


if __name__ == "__main__":
    main()
