# skin.estuary.lg (Estuary LG)

Kodi's Estuary skin with LG webOS TV integration from
[service.webostv](https://github.com/dangerouslaser/kodi-webos-control).

## Base

- Estuary 4.1.0 from Kodi 22.0 RC1 (`xbmc/xbmc@63063c8e67b1`), imported unchanged.
- LibreELEC's only Estuary patch, `1014-estuary-settings-icon` (LibreELEC.tv master), so the
  Settings screen matches LibreELEC 13 builds.
- Then our changes, kept in separate commits so a newer Estuary can be merged in.

The addon id is `skin.estuary.lg`, so it installs alongside the stock Estuary.

## Changes

| Where | What |
| --- | --- |
| `xml/Home.xml` | No Kodi logo top left; power / settings / search row moved to the bottom of the side menu; the menu starts at the top and shows 9 whole items |
| `xml/Settings.xml` | Top row holds 5 tiles with **LG TV** last (shown when service.webostv is enabled); the settings grid stays 4 per row, centred |
| `xml/Includes.xml` | `SettingsPanel` tiles scaled to 85% (340×221) so the top row fits 5; includes `Includes_LGTV.xml` |
| `xml/Custom_1120_LGTV.xml` | LG TV page, laid out like Estuary's settings pages: categories on the left (TV, Picture, TV integration, Connection), options on the right, help text for the focused option, TV model and connection at the bottom left |
| `xml/Includes_LGTV.xml` | Variables for the LG TV page |
| `media/icons/settings/lgtv.png` | Tile icon (LG logo) |
| `language/resource.language.en_gb/strings.po` | Strings 31900–31999 |

`Custom_1120_LGTV.xml` and `Includes_LGTV.xml` are generated: edit `tools/gen_lgtv.py` and run
`python3 tools/gen_lgtv.py`. Option labels and help text come from the addon's own strings
(`$ADDON[service.webostv …]`), so they stay in sync with its settings.

TV controls are disabled while the TV isn't connected. Needs service.webostv 0.4.5 or newer.

## Dev deploy

`scripts/deploy.sh` copies the skin to the Kodi box over SSH and reloads it
(`KODI_HOST`, default 192.168.1.175).

## Build

```sh
python3 scripts/build_zip.py   # -> dist/skin.estuary.lg-<version>.zip
```

Install from zip in Kodi, then *Settings → Interface → Skin → Estuary LG*.

## License

Same as Estuary: GPL-2.0 for code, CC BY-SA 4.0 for media.
