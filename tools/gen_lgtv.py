"""Generate xml/Custom_1120_LGTV.xml (the LG TV settings page).

Layout mirrors SettingsCategory.xml: categories on the left, the selected
category's options on the right, help text at the bottom. Values come from
service.webostv's WebOS.* properties and its add-on settings.

    python3 tools/gen_lgtv.py
"""

from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "xml" / "Custom_1120_LGTV.xml"
INCLUDES = OUT.with_name("Includes_LGTV.xml")
ADDON = "service.webostv"
P = "Window(Home).Property"
CONNECTED = f"String.IsEqual({P}(WebOS.Connected),true)"
CAT = "Window.Property(lgtv_category)"
# Older webOS (e.g. 5.5) won't report the picture mode, so presets are off there.
PICTURE_OK = f"!String.IsEqual({P}(WebOS.PictureSupported),false)"


def s(n: int) -> str:
    return f"$LOCALIZE[{n}]"


def a(n: int) -> str:
    return f"$ADDON[{ADDON} {n}]"


def run(*args: str) -> str:
    return f"RunScript({ADDON},{','.join(args)})"


def setting_bool(key: str) -> str:
    return f"Addon.SettingBool({ADDON},{key})"


# (category id, label, rows). Row kinds:
#   ("button", id, label, onclick, label2, enable, help)
#   ("radio", id, label, selected, onclick, enable, help)
#   ("header", label)
CATEGORIES = [
    ("tv", s(31917), [
        ("button", 100, s(31902), run("ui", "input"), f"$INFO[{P}(WebOS.AppTitle)]", CONNECTED, ""),
        ("button", 101, s(31903), run("ui", "app"), "", CONNECTED, ""),
        ("button", 102, s(31904), run("ui", "sound_output"), f"$INFO[{P}(WebOS.SoundOutputLabel)]", CONNECTED, ""),
        ("button", 103, s(31905), run("ui", "volume"), f"$INFO[{P}(WebOS.Volume)]", CONNECTED, ""),
        ("radio", 104, s(31906), f"String.IsEqual({P}(WebOS.Muted),true)",
         [("", run("mute", "toggle"))], CONNECTED, ""),
        ("radio", 105, s(31907), f"String.IsEqual({P}(WebOS.ScreenOn),true)",
         [(f"String.IsEqual({P}(WebOS.ScreenOn),true)", run("screen", "off")),
          (f"!String.IsEqual({P}(WebOS.ScreenOn),true)", run("screen", "on"))], CONNECTED, s(31926)),
        ("button", 106, s(31909), run("ui", "remote"), "", CONNECTED, ""),
        ("button", 107, s(31919), run("ui", "toast"), "", CONNECTED, ""),
        ("button", 108, s(31908), run("power_off"), "", CONNECTED, ""),
    ]),
    ("picture", s(31922), [
        ("note", s(31935), f"String.IsEqual({P}(WebOS.PictureReadable),false)"),
        ("button", 200, s(31901), run("ui", "picture_preset"), f"$INFO[{P}(WebOS.PicturePresetLabel)]", f"{CONNECTED} + {PICTURE_OK}", s(31927)),
        ("header", s(31921)),
        ("radio", 201, a(32031), setting_bool("rules_enabled"), [("", run("setting", "rules_enabled"))], PICTURE_OK, a(32081)),
        ("button", 202, a(32032), run("choose_preset", "sdr", "stay"), f"$INFO[{P}(WebOS.Rule.SDR)]", f"{setting_bool('rules_enabled')} + {PICTURE_OK}", s(31928)),
        ("button", 203, a(32033), run("choose_preset", "hdr10", "stay"), f"$INFO[{P}(WebOS.Rule.HDR10)]", f"{setting_bool('rules_enabled')} + {PICTURE_OK}", s(31928)),
        ("button", 204, a(32034), run("choose_preset", "hlg", "stay"), f"$INFO[{P}(WebOS.Rule.HLG)]", f"{setting_bool('rules_enabled')} + {PICTURE_OK}", s(31928)),
        ("button", 205, a(32035), run("choose_preset", "dolbyvision", "stay"), f"$INFO[{P}(WebOS.Rule.DolbyVision)]", f"{setting_bool('rules_enabled')} + {PICTURE_OK}", s(31928)),
        ("radio", 206, a(32036), setting_bool("restore_on_stop"), [("", run("setting", "restore_on_stop"))], f"{setting_bool('rules_enabled')} + {PICTURE_OK}", a(32086)),
    ]),
    ("integration", a(32200), [
        ("button", 300, a(32201), run("choose_kodi_input", "stay"), "$VAR[LGTVKodiInput]", "", a(32251)),
        ("button", 301, a(32203), run("setting", "on_tv_off"), "$VAR[LGTVOnTvOff]", "", a(32253)),
        ("button", 302, a(32204), run("setting", "on_switch_away"), "$VAR[LGTVOnSwitchAway]", "", a(32254)),
        ("radio", 303, a(32205), setting_bool("resume_on_return"), [("", run("setting", "resume_on_return"))],
         f"Integer.IsEqual(Addon.SettingInt({ADDON},on_switch_away),1)", a(32255)),
        ("radio", 304, a(32206), setting_bool("transparent_control"), [("", run("setting", "transparent_control"))], "", a(32256)),
    ]),
    ("connection", s(31910), [
        ("button", 400, s(31911), run("ui", "status"), "$VAR[LGTVConnectionText]", "", ""),
        ("button", 401, s(31912), run("ui", "find_tv"), f"$INFO[{P}(WebOS.ConfiguredHost)]", "", a(32056)),
        ("radio", 402, a(32011), setting_bool("toast_on_connect"), [("", run("setting", "toast_on_connect"))], "", a(32061)),
        ("button", 403, s(31913), run("ui", "repair"), "", "", a(32071)),
        ("button", 404, s(31914), f"Addon.OpenSettings({ADDON})", "", "", ""),
    ]),
]


def row(r: tuple, t: str) -> str:
    kind = r[0]
    if kind == "note":
        return f"""{t}<control type="label">
{t}	<width>1390</width>
{t}	<height>80</height>
{t}	<textoffsetx>40</textoffsetx>
{t}	<label>{r[1]}</label>
{t}	<aligny>center</aligny>
{t}	<font>font12</font>
{t}	<textcolor>grey</textcolor>
{t}	<visible>{r[2]}</visible>
{t}</control>"""
    if kind == "header":
        return f"""{t}<control type="label">
{t}	<width>1390</width>
{t}	<height>70</height>
{t}	<textoffsetx>40</textoffsetx>
{t}	<label>{r[1]}</label>
{t}	<aligny>bottom</aligny>
{t}	<font>font25_title</font>
{t}	<textcolor>button_focus</textcolor>
{t}</control>"""
    if kind == "button":
        _, cid, label, onclick, label2, enable, _help = r
        lines = [f'<control type="button" id="{cid}">', "\t<width>1390</width>",
                 f"\t<label>{label}</label>"]
        if label2:
            lines.append(f"\t<label2>{label2}</label2>")
        lines.append(f"\t<onclick>{onclick}</onclick>")
    else:
        _, cid, label, selected, onclicks, enable, _help = r
        lines = [f'<control type="radiobutton" id="{cid}">', "\t<width>1390</width>",
                 f"\t<label>{label}</label>", f"\t<selected>{selected}</selected>"]
        for cond, action in onclicks:
            c = f' condition="{cond}"' if cond else ""
            lines.append(f"\t<onclick{c}>{action}</onclick>")
    if enable:
        lines.append(f"\t<enable>{enable}</enable>")
    lines += ["\t<include>DefaultSettingButton</include>", "</control>"]
    return "\n".join(t + line for line in lines)


def build() -> str:
    t3, t4 = "\t\t\t", "\t\t\t\t"
    first_ids = {cat: next(r[1] for r in rows if r[0] not in ("header", "note")) for cat, _l, rows in CATEGORIES}

    cat_buttons = []
    for i, (cat, label, _rows) in enumerate(CATEGORIES):
        onright = f"Control.SetFocus({first_ids[cat] // 100 * 10 + 500})"
        cat_buttons.append(f"""{t4}<control type="button" id="{21 + i}">
{t4}	<width>470</width>
{t4}	<height>85</height>
{t4}	<textoffsetx>40</textoffsetx>
{t4}	<aligny>center</aligny>
{t4}	<font>font37</font>
{t4}	<label>{label}</label>
{t4}	<onfocus>SetProperty(lgtv_category,{cat})</onfocus>
{t4}	<onright>{onright}</onright>
{t4}	<texturefocus colordiffuse="button_focus">lists/focus.png</texturefocus>
{t4}	<texturenofocus />
{t4}</control>""")
        # Keep the current category highlighted while the options have focus.
    cat_marks = "\n".join(f"""{t3}<control type="image">
{t3}	<left>0</left>
{t3}	<top>{130 + 85 * i}</top>
{t3}	<width>470</width>
{t3}	<height>85</height>
{t3}	<texture colordiffuse="button_alt_focus">lists/focus.png</texture>
{t3}	<visible>String.IsEqual({CAT},{cat}) + !Control.HasFocus({21 + i})</visible>
{t3}</control>""" for i, (cat, _l, _r) in enumerate(CATEGORIES))

    lists = []
    for i, (cat, _label, rows) in enumerate(CATEGORIES):
        gid = first_ids[cat] // 100 * 10 + 500
        body = "\n".join(row(r, t4 + "\t") for r in rows)
        lists.append(f"""{t3}<control type="grouplist" id="{gid}">
{t3}	<top>133</top>
{t3}	<left>470</left>
{t3}	<right>60</right>
{t3}	<bottom>137</bottom>
{t3}	<pagecontrol>60</pagecontrol>
{t3}	<onleft>Control.SetFocus({21 + i})</onleft>
{t3}	<onright>60</onright>
{t3}	<onup>{gid}</onup>
{t3}	<ondown>{gid}</ondown>
{t3}	<visible>String.IsEqual({CAT},{cat})</visible>
{t3}	<include>Visible_Fade</include>
{body}
{t3}</control>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!-- GENERATED by tools/gen_lgtv.py; edit that and re-run.
     skin.estuary.lg: LG TV settings page (Settings > LG TV). Layout follows
     SettingsCategory.xml; values come from service.webostv. -->
<window id="1120">
	<defaultcontrol always="true">21</defaultcontrol>
	<onload>SetProperty(lgtv_category,tv)</onload>
	<backgroundcolor>background</backgroundcolor>
	<controls>
		<include>DefaultBackground</include>
		<control type="multiimage">
			<depth>DepthBackground</depth>
			<include>FullScreenDimensions</include>
			<aspectratio>scale</aspectratio>
			<animation effect="fade" start="0" end="100" time="400" reversible="true" condition="!Window.Previous(Settings)">WindowOpen</animation>
			<animation effect="fade" start="100" end="0" time="300" reversible="true" condition="!Window.Next(Settings)">WindowClose</animation>
			<imagepath colordiffuse="35FFFFFF">$INFO[Skin.String(HomeFanart.path)]settings$INFO[Skin.String(HomeFanart.ext)]</imagepath>
			<visible>!Player.HasMedia + !String.IsEmpty(Skin.String(HomeFanart.path))</visible>
		</control>
		<control type="group">
			<include>OpenClose_Right</include>
{chr(10).join(lists)}
			<control type="image">
				<left>470</left>
				<top>130</top>
				<right>0</right>
				<height>2</height>
				<texture colordiffuse="button_focus" border="2">dialogs/separator-grey.png</texture>
			</control>
			<control type="image">
				<left>470</left>
				<bottom>135</bottom>
				<right>0</right>
				<height>2</height>
				<texture colordiffuse="button_focus" border="2">dialogs/separator-grey.png</texture>
			</control>
			<control type="textbox">
				<description>help for the focused option</description>
				<left>510</left>
				<bottom>25</bottom>
				<right>60</right>
				<height>104</height>
				<font>font12</font>
				<align>justify</align>
				<textcolor>button_focus</textcolor>
				<label>$VAR[LGTVHelp]</label>
				<autoscroll time="3000" delay="5000" repeat="5000">true</autoscroll>
			</control>
		</control>
		<control type="group">
			<depth>DepthContentPanel</depth>
			<include>OpenClose_Left</include>
			<include content="ContentPanel">
				<param name="width" value="530" />
			</include>
{cat_marks}
			<control type="grouplist" id="3">
				<left>0</left>
				<top>130</top>
				<width>470</width>
				<height>810</height>
				<onup>3</onup>
				<ondown>3</ondown>
{chr(10).join(cat_buttons)}
			</control>
			<control type="image">
				<left>20</left>
				<bottom>110</bottom>
				<width>230</width>
				<height>230</height>
				<texture>icons/settings/lgtv.png</texture>
				<aspectratio>keep</aspectratio>
			</control>
			<control type="label">
				<left>40</left>
				<bottom>105</bottom>
				<width>430</width>
				<height>40</height>
				<label>$INFO[{P}(WebOS.Model)]</label>
				<font>font12</font>
				<textcolor>grey</textcolor>
			</control>
			<control type="label">
				<left>40</left>
				<bottom>65</bottom>
				<width>430</width>
				<height>40</height>
				<label>$VAR[LGTVConnectionText]</label>
				<font>font12</font>
			</control>
		</control>
		<control type="group">
			<right>0</right>
			<top>133</top>
			<bottom>137</bottom>
			<width>60</width>
			<control type="scrollbar" id="60">
				<right>0</right>
				<top>0</top>
				<bottom>0</bottom>
				<width>12</width>
				<orientation>vertical</orientation>
				<texturesliderbackground />
				<animation effect="fade" start="0" end="100" time="200" delay="300">Visible</animation>
				<animation effect="fade" start="100" end="0" time="200">Hidden</animation>
			</control>
		</control>
		<include content="TopBar">
			<param name="breadcrumbs_label" value="$LOCALIZE[5] / $LOCALIZE[31900]" />
		</include>
		<include>BottomBar</include>
	</controls>
</window>
"""


def build_includes() -> str:
    helps = [(r[1], r[-1]) for _c, _l, rows in CATEGORIES for r in rows if r[0] in ("button", "radio") and r[-1]]
    help_var = "\n".join(f'\t\t<value condition="Control.HasFocus({cid})">{text}</value>' for cid, text in helps)
    tv_off = "\n".join(
        f'\t\t<value condition="Integer.IsEqual(Addon.SettingInt({ADDON},on_tv_off),{i})">{a(32210 + i)}</value>'
        for i in range(4))
    away = "\n".join(
        f'\t\t<value condition="Integer.IsEqual(Addon.SettingInt({ADDON},on_switch_away),{i})">{a(32210 + i)}</value>'
        for i in range(3))
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!-- GENERATED by tools/gen_lgtv.py. Variables for Custom_1120_LGTV.xml. -->
<includes>
	<variable name="LGTVHelp">
{help_var}
	</variable>
	<variable name="LGTVConnectionText">
		<value condition="{CONNECTED}">[COLOR button_focus]{s(31915)}[/COLOR]$INFO[{P}(WebOS.Host), · ]</value>
		<value>[COLOR red]{s(31916)}[/COLOR]</value>
	</variable>
	<variable name="LGTVKodiInput">
		<value condition="!String.IsEmpty({P}(WebOS.KodiInput))">$INFO[{P}(WebOS.KodiInput)]</value>
		<value>{a(32309)}</value>
	</variable>
	<variable name="LGTVOnTvOff">
{tv_off}
	</variable>
	<variable name="LGTVOnSwitchAway">
{away}
	</variable>
</includes>
"""


if __name__ == "__main__":
    OUT.write_text(build())
    INCLUDES.write_text(build_includes())
    print(OUT, INCLUDES, sep="\n")
