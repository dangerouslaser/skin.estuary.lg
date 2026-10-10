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
| `xml/Settings.xml` | **LG TV** tile (8th slot of the lower grid), shown when service.webostv is enabled |
| `xml/Custom_1120_LGTV.xml` | LG TV page: live status (model, connection, power, input, preset, volume) and settings-style rows for picture preset, input, apps, sound output, volume, mute, screen, remote, message, power off, status, Find TV, re-pair, add-on settings |
| `xml/Variables.xml` | `LGTVConnectionLabel`, `LGTVMutedLabel` |
| `media/icons/settings/lgtv.png` | Tile icon |
| `language/resource.language.en_gb/strings.po` | Strings 31900–31999 |

TV controls are disabled while the TV isn't connected. The page needs service.webostv 0.4.4 or
newer (properties `WebOS.Model`, `WebOS.PicturePresetLabel`, `WebOS.SoundOutputLabel`, and
`RunScript(service.webostv,ui,<page>)`).

## Build

```sh
python3 scripts/build_zip.py   # -> dist/skin.estuary.lg-<version>.zip
```

Install from zip in Kodi, then *Settings → Interface → Skin → Estuary LG*.

## License

Same as Estuary: GPL-2.0 for code, CC BY-SA 4.0 for media.
