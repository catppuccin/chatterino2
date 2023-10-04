import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, TypeAlias
from urllib.request import urlretrieve

from catppuccin import Colour, Flavour  # type: ignore
from jsonschema import validate

icon_theme_t: TypeAlias = Literal["dark", "light"]
json_t: TypeAlias = dict[str, "json_t"] | str


@dataclass(frozen=True, kw_only=True)
class NamedColour(object):
    accent: Colour
    name: str


@dataclass(frozen=True, kw_only=True)
class NamedFlavour(object):
    flavour: Flavour
    icon_theme: icon_theme_t
    name: str


SCHEMA_URL: str = "https://raw.githubusercontent.com/Chatterino/chatterino2/master/docs/ChatterinoTheme.schema.json"


def main() -> None:
    schema: str = retrieve_via_http(SCHEMA_URL)

    flavours: list[NamedFlavour] = [
        NamedFlavour(flavour=Flavour.frappe(), icon_theme="light", name="frappe"),
        NamedFlavour(flavour=Flavour.latte(), icon_theme="dark", name="latte"),
        NamedFlavour(flavour=Flavour.macchiato(), icon_theme="light", name="macchiato"),
        NamedFlavour(flavour=Flavour.mocha(), icon_theme="light", name="mocha"),
    ]

    for named_flavour in flavours:
        accents: list[NamedColour] = [
            NamedColour(accent=named_flavour.flavour.rosewater, name="rosewater"),
            NamedColour(accent=named_flavour.flavour.flamingo, name="flamingo"),
            NamedColour(accent=named_flavour.flavour.pink, name="pink"),
            NamedColour(accent=named_flavour.flavour.mauve, name="mauve"),
            NamedColour(accent=named_flavour.flavour.red, name="red"),
            NamedColour(accent=named_flavour.flavour.maroon, name="maroon"),
            NamedColour(accent=named_flavour.flavour.peach, name="peach"),
            NamedColour(accent=named_flavour.flavour.yellow, name="yellow"),
            NamedColour(accent=named_flavour.flavour.green, name="green"),
            NamedColour(accent=named_flavour.flavour.teal, name="teal"),
            NamedColour(accent=named_flavour.flavour.sky, name="sky"),
            NamedColour(accent=named_flavour.flavour.sapphire, name="sapphire"),
            NamedColour(accent=named_flavour.flavour.blue, name="blue"),
            NamedColour(accent=named_flavour.flavour.lavender, name="lavender"),
        ]

        for named_accent in accents:
            path: Path = Path(f"dist/{named_flavour.name}-{named_accent.name}.json")

            theme: json_t = generate_theme(
                named_flavour.flavour,
                named_accent.accent,
                named_flavour.icon_theme,
            )

            validate(instance=theme, schema=json.loads(schema))

            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(theme, indent=2, sort_keys=True))


def retrieve_via_http(url: str) -> str:
    if not url.startswith(("http:", "https:")):
        raise ValueError("URL must start with 'http:' or 'https:'")

    location, headers = urlretrieve(url)
    with open(location) as response:
        return response.read()


def generate_theme(
    flavour: Flavour,
    accent: Colour,
    icon_theme: icon_theme_t,
) -> json_t:
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
        "$schema": SCHEMA_URL,
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
                    "text": f"#{flavour.subtext1.hex}",
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