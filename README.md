<h3 align="center">
  <img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/logos/exports/1544x1544_circle.png" width="100" alt="Logo"/>
  <br/>
  <img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/misc/transparent.png" height="30" width="0px"/>
  Catppuccin for <a href="https://github.com/chatterino/chatterino2">Chatterino 2</a>
  <img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/misc/transparent.png" height="30" width="0px"/>
</h3>

<p align="center">
  <a href="https://github.com/fruzitent/chatterino2/stargazers">
    <img src="https://img.shields.io/github/stars/fruzitent/chatterino2?colorA=363a4f&colorB=b7bdf8&style=for-the-badge">
  </a>
  <a href="https://github.com/fruzitent/chatterino2/issues">
    <img src="https://img.shields.io/github/issues/fruzitent/chatterino2?colorA=363a4f&colorB=f5a97f&style=for-the-badge">
  </a>
  <a href="https://github.com/fruzitent/chatterino2/contributors">
    <img src="https://img.shields.io/github/contributors/fruzitent/chatterino2?colorA=363a4f&colorB=a6da95&style=for-the-badge">
  </a>
</p>

![catwalk](assets/catwalk.webp)

## Previews

<details>
<summary>🌻 Latte</summary>

![latte](assets/latte.webp)
</details>

<details>
<summary>🪴 Frappé</summary>

![frappe](assets/frappe.webp)
</details>

<details>
<summary>🌺 Macchiato</summary>

![macchiato](assets/macchiato.webp)
</details>

<details>
<summary>🌿 Mocha</summary>

![mocha](assets/mocha.webp)
</details>

## Usage

1. Copy files into [themesDirectory](https://github.com/Chatterino/chatterino2/blob/38a7ce695485e080f6e98e17c9b2a01bcbf17744/src/singletons/Paths.hpp#L41)

2. Apply changes to [settingsDirectory/settings.json](https://github.com/Chatterino/chatterino2/blob/38a7ce695485e080f6e98e17c9b2a01bcbf17744/src/singletons/Paths.hpp#L20)

    <details>
    <summary>2.1. Update active theme</summary>

    ```json
    {
      "appearance": {
        "theme": {
          "name": "theme-accent.json"
        },
      }
    }
    ```

    </details>

    <details>
    <summary>2.2. [Optional] Set "most recent message line" color to preferred accent</summary>

    ```json
    {
      "appearance": {
        "messages": {
          "lastMessageColor": "#AARRGGBB",
          "showLastMessageIndicator": true
        }
      }
    }
    ```

    </details>
