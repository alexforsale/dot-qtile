import os
from collections.abc import Callable
import shutil

import libqtile.resources
from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Output, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"

terminal = guess_terminal()

def guess_browser():
    """"Get currently available browser."""
    for b in ["firefox", "brave-browser", "google-chrome-stable"]:
        if shutil.which(b):
            return b


browser = guess_browser()

mail = "thunderbird"

filemanager = "thunar"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key(["mod1"], "Tab", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.screen.toggle_group(), desc="Toggle between groups"),
    Key([mod, "mod1"], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    # Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "bracketleft", lazy.to_screen(0)),
    Key([mod], "bracketright", lazy.to_screen(1)),

    Key([], "XF86AudioRaiseVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +10%"), desc="Raise Volume Up"),
    Key([], "XF86AudioLowerVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -10%"), desc="Raise Volume Down"),
    Key([], "XF86AudioMute",
        lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"), desc="Toggle Audio Mute"),
    Key([], "XF86AudioMicMute",
        lazy.spawn("pactl set-source-mute @DEFAULT_SOURCE@ toggle"), desc="Toggle Audio Mic Mute"),

    Key([], "XF86AudioPlay",
        lazy.spawn("playerctl play-pause"), desc="Toggle play/pause"),
    Key([], "XF86AudioPrev",
        lazy.spawn("playerctl previous"), desc="Previous"),
    Key([], "XF86AudioNext",
        lazy.spawn("playerctl next"), desc="Next"),
    # TODO: XF86Tools for Audio
    Key([], "XF86Calculator",
        lazy.spawn("rofi -show calc -modi calc -no-show-match -no-sort"), desc="Calculator"),

    Key([], "XF86HomePage",
        lazy.spawn(browser), desc="Browser"),
    Key([mod, "mod1"], "b",
        lazy.spawn(browser), desc="Browser"),
    Key([], "XF86Mail",
        lazy.spawn(mail), desc="Mail Client"),
    Key([], "XF86Search",
        lazy.spawn("rofi-search"), desc="Search"),

    Key([], "Print",
        lazy.spawn("flameshot gui"), desc="flameshot"),

    Key([mod, "mod1"], "v", lazy.spawn("neovide"), desc="neovide"),
    Key([mod, "mod1"], "p", lazy.spawn("rofi-pass"), desc="rofi pass"),
    Key([mod, "mod1"], "n", lazy.spawn("emacsclient -c -a emacs"), desc="emacs"),
    Key([mod, "mod1"], "s", lazy.spawn("screenkey"), desc="screenkey"),

    Key([mod], "e", lazy.spawn(filemanager), desc="file-manager"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod, "shift"], "Return", lazy.spawn(f"{terminal} -e tmux new -A -s main"), desc="Tmux"),
    Key(["mod1"], "F4", lazy.window.kill(), desc="kill focused window"),
    Key([mod], "F4", lazy.window.kill(), desc="kill focused window"),
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc="rofi menu"),
    Key([mod], "c",
        lazy.spawn("rofi -modi 'clipboard:greenclip print' -show clipboard"),
        desc="rofi greenclip"),
    Key([mod, "shift"], "w",
        lazy.spawn("rofi -show windowcd"), desc="rofi windowcd"),
    Key([mod], "w",
        lazy.spawn("rofi -show window"), desc="rofi window"),
    Key([mod], "q",
        lazy.spawn("rofi -show p -modi p:'rofi-power-menu --symbols-font \"Symbols Nerd Font Mono\"' -font 'OverpassM Nerd Font Mono' -theme catppuccin-default -theme-str 'window {width: 8em;} listview {lines: 6;}'"), desc="rofi-power-menu"),
    Key([mod], "period", lazy.spawn("rofimoji"), desc="rofimoji"),
    # Key([mod, "shift"], "t", lazy.spawn(ocr()), desc="ocr"),
]

for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="OverpassM Nerd Font Mono",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

logo = os.path.join(os.path.dirname(libqtile.resources.__file__), "logo.png")
screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.CurrentScreen(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # widget.TextBox("default config", name="default"),
                # widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                # widget.TunedManager(),
                widget.CapsNumLockIndicator(),
                widget.ThermalZone(),
                widget.PulseVolume(),
                # widget.Volume(
                #     volume_down_command="pactl set-sink-volume @DEFAULT_SINK@ -10%",
                #     volume_up_command="pactl set-sink-volume @DEFAULT_SINK@ +10%",
                #     volume_app="pavucontrol",
                # ),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
                widget.QuickExit(),
                widget.Systray(),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        #background="#000000",
        wallpaper="assets/img/arch-black-4k.png",
        #wallpaper_mode="fill",
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
    Screen(
        bottom=bar.Bar(
            [
                widget.WindowName(),
                widget.CurrentScreen(),
                # widget.Canto(),
            ],
            24,
        ),
        wallpaper="assets/img/various-arch-1-4k.png",
        #wallpaper_mode="center",
    ),
]

# Instead of screens, you can define a function here to specify which Screen
# should correspond to which Output.
fake_screens: list[Screen] | None = None

# Instead of screens or fake screens, you can define a function here that
# returns a list of Screen objects based on the list of Outputs; that way you
# can decide based on e.g. the number of screens, or which ports are plugged
# in exactly what do render in each bar for each screen.
generate_screens: Callable[[list[Output]], list[Screen]] | None = None

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
focus_previous_on_window_remove = False
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

idle_timers = []  # type: list
idle_inhibitors = []  # type: list

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)

STARTUP_COMMANDS = [
    "dbus-update-activation-environment --all"
    "xsetroot -cursor_name left_ptr",
    "xset r rate 500 25",
    "/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &",
    "picom -b &",
    "greenclip daemon>/dev/null &",
    "thunar --daemon &",
    "unclutter &",
    "nm-applet & ",
    "~/.fehbg &",
    "emacs --daemon &",
    "xsettingsd &"
]


@hook.subscribe.startup_once
def autostart():
    """Stuffs to autostart."""
    for cmd in STARTUP_COMMANDS:
        os.system(cmd)
