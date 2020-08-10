#
# _____ _            _   _ _
#|_   _| |          | | | (_)
#  | | | |__   ___  | |_| |___   _____
#  | | | '_ \ / _ \ |  _  | \ \ / / _ \
#  | | | | | |  __/ | | | | |\ V /  __/  _______
#  \_/ |_| |_|\___| \_| |_/_| \_/ \___| |_______|
#	   jane.pnx9@gmail.com
#
# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook

from typing import List  # noqa: F401

mod = "mod4"


###  https://github.com/qtile/qtile/blob/master/libqtile/xkeysyms.py -> for keybindings

###  Modules
import os
import re
import subprocess
import socket

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

spawn_term = "st"

wallpaper = os.path.expanduser('~/Pictures/Wallpapers/641062.jpg')
###  Commands
class Commands(object):
	global spawn_term
	firefox = 'firefox'
	firefox_dev = 'firefox-developer-edition'
	virtualbox = 'virtualbox'
	filesystem_nautilus = 'nautilus -s /home/pnx9/'
	filesystem_ranger = spawn_term+' -e sh ./.config/qtile/ranger.sh'
	launcher = 'dmenu_run -p "Run: "'
	bluetooth_on = 'bluetooth on'
	bluetooth_off = 'bluetooth off'
	lockscreen = 'i3lock -t -i Pictures/Wallpapers/screenlock.png'
        ## 'XF86AudioLowerVolume': 0x1008FF11,
        ## 'XF86AudioMute': 0x1008FF12,
        ## 'XF86AudioRaiseVolume': 0x1008FF13,
	## /usr/bin/pulseaudio-ctl  could be better for toggling mute (mute / mute-input)
	volume_mute = '/usr/bin/pulseaudio-ctl mute'
	volume_down = 'amixer -q -c 0 sset Master 5dB-'
	volume_up = 'amixer -q -c 0 sset Master 5dB+'
	mic_toggle = '/usr/bin/pulseaudio-ctl mute-input' # still not/'XF86AudioMicMute': 0x1008FFB2,
	# 'XF86MonBrightnessUp': 0x1008FF02,
        # 'XF86MonBrightnessDown': 0x1008FF03,
	#  xbacklight can have steps, but something wrong with RANDR ??
	brightness_up = 'xrandr --output eDP-1-1 --brightness 1'
	brightness_down = 'xrandr --output eDP-1-1 --brightness .50'
	## 'XF86TouchpadToggle': 0x1008FFA9,
        ## 'XF86TouchpadOn': 0x1008FFB0,
        ## 'XF86TouchpadOff': 0x1008FFB1,
	touchpad_toggle = '' # xinput
	# https://help.ubuntu.com/community/SynapticsTouchpad/ShortcutKey
	# https://help.ubuntu.com/community/SynapticsTouchpad
	screenshot = 'gnome-screenshot' #XF86ScreenSaver??
	double_monitor = 'xrandr --output eDP-1-1 --auto --primary --left-of HDMI-0'
	kb_backlight = '' #xbacklight
	kb_layout_toggle = './kblayout'

###  setup defaults
color = dict(
	purple='#8d62a9',
	white='#d3ebe9',
	green='#ccff99',
	black='#0a0a0a',
	light_blue='#66d9ee',
	blue='#43ADC7',
	red='#c33027',
	yellow='#edb54b',
	grey='#282a36',
	light_grey='#434758',
	)

layout_defaults = dict(
	border_width = 3,
	margin = 10,
	border_focus = color['blue'],
	border_normal = color['white']
	)

bar_defaults = dict(
	size = 24,
	margin = 1,
	background = color['black'],
	)

widget_defaults = dict(
    font='Source Code Pro',
    fontsize=12,
    padding=5,
    background= color['black']
    )

keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),

    # Move windows up or down in current stack  -> same as Mod+space
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),

    # toggle the Terminal
    Key([mod], "Return", lazy.spawn("st")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),

    # qtile controls
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod, "control"], "l", lazy.spawn(Commands.lockscreen)),
    Key([mod, "control"], 'f', lazy.window.toggle_floating()),
    Key([mod], "r", lazy.spawncmd()),

###  COMMANDS
    Key([mod, "shift"], "r", lazy.spawn(Commands.launcher)),
    Key([mod, "shift"], "b", lazy.spawn(Commands.bluetooth_on)),
    Key([mod, "shift"], "q", lazy.spawn(Commands.bluetooth_off)),
    # Display Fix: Double Monitor
    Key([mod, "shift"], "x", lazy.spawn(Commands.double_monitor),
	desc='resolve the displays problem using xrandr'),

    # toggle file system
    Key([mod], "g", lazy.spawn(Commands.filesystem_ranger)),
    Key([mod], "h", lazy.spawn(Commands.filesystem_nautilus)),


    # toggle firefox / firefox-dev-edition
    Key([mod], "d", lazy.spawn(Commands.firefox_dev)),
    Key([mod], "f", lazy.spawn(Commands.firefox)),

    # virtualbox
    Key([mod], "v", lazy.spawn(Commands.virtualbox)),

    # volume
    Key([], "XF86AudioLowerVolume", lazy.spawn(Commands.volume_down)),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(Commands.volume_up)),
    Key([], "XF86AudioMute", lazy.spawn(Commands.volume_mute)),

    # Mic
    Key([], "XF86AudioMicMute", lazy.spawn(Commands.mic_toggle)),
    # brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn(Commands.brightness_up)),
    Key([], "XF86MonBrightnessDown", lazy.spawn(Commands.brightness_down)),
    Key([mod], "p", lazy.spawn(Commands.screenshot)),

    # Keyboard Layout -> toggle layout problem
    # Key([mod], "", lazy.spawn(Commands.kb_layout_toggle)),
]

groups = [Group(i) for i in "1234"]

for i in groups:
    if (i == "4"):
        layout = "floating"
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True)),
        # Or, use below if you prefer not to switch to that group.

        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

layouts = [
    layout.Max(**layout_defaults),
    layout.Stack(num_stacks=2,
	**layout_defaults),
    layout.MonadTall(**layout_defaults),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Columns(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(**layout_defaults),
]

floating_layout = layout.Floating(
        auto_float_types=(
                'notification',
                'toolbar',
                'splash',
                'dialog',
        ),
        float_rules=[
                # Run the utility of `xprop` to see the wm class and name of an X client.
                {'wmclass': 'confirm'},
                {'wmclass': 'download'},
                {'wmclass': 'error'},
                {'wmclass': 'file_progress'},
                {'wmclass': 'notification'},
                {'wmclass': 'splash'},
                {'wmclass': 'toolbar'},
                {'wmclass': 'confirmreset'},  # gitk
                {'wmclass': 'makebranch'},  # gitk
                {'wmclass': 'maketag'},  # gitk
                {'wname': 'branchdialog'},  # gitk
                {'wname': 'pinentry'},  # GPG key password entry
                {'wmclass': 'ssh-askpass'},  # ssh-askpass
        ],
        **layout_defaults
)


extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
	         widget.CurrentLayoutIcon(
                        foreground = color['light_blue'],
                        custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
                        padding = 0,
                        scale=0.7
                        ),
                 widget.CurrentLayout(
                        padding = 5
                        ),
		 widget.KeyboardLayout(
			padding = 5,
			configured_keyboards = ['us', 'ara'],
			font = "Source Code Pro"
                        foreground = color['light_blue'],
			),
 		 widget.LaunchBar(
                        padding = 5,
                        progs = [('Calendar', 'google-calendar -h', 'Google Calendar'>
                        ),
		 widget.GroupBox(font="Ubuntu Bold",
                        fontsize = 9,
                        margin_y = 3,
                        margin_x = 0,
                        padding_y = 5,
                        padding_x = 5,
                        borderwidth = 3,
                        active = color['white'],
                        inactive = color['white'],
                        rounded = False,
                        highlight_color = color['grey'],
                        highlight_method = "line",
                        this_current_screen_border = color['green'],
                        this_screen_border = color['purple'],
                        other_current_screen_border = color['light_grey'],
                        other_screen_border = color['grey'],
                        foreground = color['white'],
                        font = "Source Code Pro",
                        ),
		widget.WindowName(
                        foreground = color['green'],
                        background = color['black'],
                        padding = 10
                        ),
		widget.Notify(
			margin = 6,
			default_timeout = 3,
			font = "Source Code Pro",
			markup = True,
			foreground = '#fa2772',
			),
		widget.Prompt(prompt=prompt,
                        font="Source Code Pro",
                        padding=10,
                        cursor = True,
                        cursor_color = 'bef098',
                        bell_style = 'None'
                        ),
	                widget.TextBox(
			foreground= color['light_blue'],
                        text=" 🖬",
                        padding = 0,
                        fontsize=16
                        ),
                widget.Memory(
                        padding = 5
                        ),
		widget.TextBox(
			foreground = color['light_blue'],
                        text=" 🌡",
                        padding = 1,
                        fontsize=11
                        ),
		widget.ThermalSensor(
                        padding = 5
                        ),
                widget.TextBox(
			foreground = color['light_blue'],
                        text=" ⟳",
                        padding = 1,
                        fontsize=16
                        ),
                widget.Pacman(
                        execute = "st",
                        update_interval = 1800,
                        ),
                widget.TextBox(
                        text="Updates",
                        padding = 5,
			),
                widget.TextBox(
                        text=" 🔊",
			foreground = color['light_blue'],
			fontsize = 16,
                        padding = 0
                        ),
                widget.Volume(
                        padding = 5
                        ),
		widget.TextBox(
			text = " ⌛",
			padding = 0,
			fontsize=16,
			foreground = color['light_blue']
			),
		widget.Battery(
			charge_char = '^',
			discharge_char = 'v',
			notify_below = 10,
			padding = 5,
			format = '{percent:2.0%}'
			),
		widget.TextBox(
			text = " ☁",
			padding = 0,
			fontsize = 18,
			foreground= color['light_blue']
			),
		widget.Net(
			interface='wlp7s0',
			format = '{down}↓↑{up}',
			),
		widget.TextBox(
			text = " 🕳",
			fontsize = 18,
			foreground = color['light_blue']
			),
		widget.Clock(
                        format="%A, %B %d  [ %H:%M ]"
                        ),
		widget.Systray(),
		widget.TextBox(
			text=' ',
			),
#               widget.QuickExit(),
            ],
	    **bar_defaults),
	wallpaper = wallpaper,
	wallpaper_mode = 'fill'
    ),
    Screen(
	top=bar.Bar([
		widget.CurrentLayoutIcon(
                        custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
                        padding = 0,
                        scale=0.7
                        ),
                widget.CurrentLayout(
                        padding = 5
                        ),
		widget.GroupBox(font="Ubuntu Bold",
                        fontsize = 9,
                        margin_y = 3,
                        margin_x = 0,
                        padding_y = 5,
                        padding_x = 5,
                        borderwidth = 3,
                        active = color['white'],
                        inactive = color['white'],
                        rounded = False,
                        highlight_color = color['grey'],
                        highlight_method = "line",
                        this_current_screen_border = color['green'],
                        this_screen_border = color['purple'],
                        other_current_screen_border = color['light_grey'],
                        other_screen_border = color['grey'],
                        foreground = color['white'],
                        background = color['black']
                        ),
                widget.WindowName(
                        foreground = color['green'],
                        background = color['black'],
                        padding = 10
                        ),

                widget.Notify(
                        margin = 6,
                        default_timeout = 3,
                        font = "Source Code Pro",
                        markup = True,
                        foreground = '#fa2772',
			),
		widget.TextBox(
                       text=" 🔊",
                        foreground = color['light_blue'],
                        fontsize = 16,
                        padding = 0
                        ),
		widget.Volume(
                        padding = 5
                        ),
                widget.TextBox(
                        text = " ⌛",
                        padding = 0,
                        fontsize=16,
                        foreground = color['light_blue']
                	),
                widget.Battery(
                        padding = 5,
                        format = '{percent:2.0%}'
                	),
                widget.TextBox(
                        text = " 🕳",
                        fontsize = 18,
                        foreground = color['light_blue']
                        ),

                widget.Clock(
                        format="%A, %B %d  [ %H:%M ]"
                        ),
		widget.Systray(),
		widget.TextBox(
			text= "  ",
			),
	    ],
	**bar_defaults
	),
	wallpaper = wallpaper,
	wallpaper_mode = 'fill'
    )
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"

################ STARTUP APPLICATIONS ########################
@hook.subscribe.startup_once
def start_once():
	subprocess.Popen(['picom', '-b']),
	subprocess.Popen(['feh --bg-center '+ wallpaper]),


# Startup applications rather than process can be put here too, Firefox, Evolution ...etc

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
