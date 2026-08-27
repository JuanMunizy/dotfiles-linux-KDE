#!/usr/bin/env python3
"""
Wallpaper Dynamic Color Scheme Generator for KDE Plasma 6.
Uses inotifywait to monitor wallpaper config changes.
Generates a matching KDE dark color scheme from dominant wallpaper colors.
"""

import os
import sys
import time
import hashlib
import subprocess
import tempfile
from pathlib import Path
from collections import Counter

try:
    from PIL import Image
except ImportError:
    print("ERROR: python-pillow not installed. Run: sudo pacman -S python-pillow", flush=True)
    sys.exit(1)

CONFIG_FILE = Path.home() / ".config" / "plasma-org.kde.plasma.desktop-appletsrc"
SCHEMES_DIR = Path.home() / ".local" / "share" / "color-schemes"
SCHEME_NAME = "WallpaperDynamic"
FALLBACK_IMAGE = "/usr/share/wallpapers/cachyos-wallpapers/north.png"
VIDEO_EXTS = {".mp4", ".mkv", ".webm", ".avi", ".mov", ".flv", ".m4v"}


def log(msg):
    print(f"[wallpaper-colors] {msg}", flush=True)


def parse_wallpaper_path(config_path):
    if not config_path.exists():
        return None
    text = config_path.read_text(errors="replace")
    video_urls = []
    image_path = None
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("LastVideo="):
            video_urls.append(line.split("=", 1)[1])
        if line.startswith("Image="):
            image_path = line.split("=", 1)[1]
    if video_urls:
        url = video_urls[-1]
        if url.startswith("file://"):
            path = url[7:]
            if os.path.isfile(path):
                return path
    if image_path and os.path.isfile(image_path):
        return image_path
    return FALLBACK_IMAGE if os.path.isfile(FALLBACK_IMAGE) else None


def extract_frame(video_path):
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    tmp.close()
    try:
        r = subprocess.run(
            ["ffmpeg", "-y", "-ss", "4", "-i", video_path,
             "-vframes", "1", "-q:v", "2", tmp.name],
            capture_output=True, timeout=20
        )
        if r.returncode == 0 and os.path.isfile(tmp.name):
            img = Image.open(tmp.name).convert("RGB")
            return img
    except Exception as e:
        log(f"ffmpeg error: {e}")
    finally:
        try:
            os.unlink(tmp.name)
        except OSError:
            pass
    return None


def load_image(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in VIDEO_EXTS:
        return extract_frame(path)
    try:
        return Image.open(path).convert("RGB")
    except Exception:
        return None


def extract_colors(img):
    small = img.copy()
    small.thumbnail((150, 150))
    q = small.quantize(colors=16, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()
    quantized = [(pal[i*3], pal[i*3+1], pal[i*3+2]) for i in range(16)]
    pixels = list(small.convert("RGB").getdata())
    freq = Counter(pixels).most_common(16)
    frequent = [c for c, _ in freq]
    return quantized + frequent


def rgb_to_hsl(r, g, b):
    rn, gn, bn = r / 255.0, g / 255.0, b / 255.0
    cmax, cmin = max(rn, gn, bn), min(rn, gn, bn)
    delta = cmax - cmin
    l = (cmax + cmin) / 2.0
    if delta == 0:
        return 0.0, 0.0, l
    s = delta / (1.0 - abs(2 * l - 1)) if 0 < l < 1 else 1.0
    if cmax == rn:
        h = 60 * (((gn - bn) / delta) % 6)
    elif cmax == gn:
        h = 60 * (((bn - rn) / delta) + 2)
    else:
        h = 60 * (((rn - gn) / delta) + 4)
    return h % 360, min(1.0, s), l


def hsl_to_rgb(h, s, l):
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    if h < 60:
        r1, g1, b1 = c, x, 0
    elif h < 120:
        r1, g1, b1 = x, c, 0
    elif h < 180:
        r1, g1, b1 = 0, c, x
    elif h < 240:
        r1, g1, b1 = 0, x, c
    elif h < 300:
        r1, g1, b1 = x, 0, c
    else:
        r1, g1, b1 = c, 0, x
    return (int((r1+m)*255), int((g1+m)*255), int((b1+m)*255))


def clamp(v):
    return max(0, min(255, v))


def boost_sat(r, g, b, amount=1.3):
    h, s, l = rgb_to_hsl(r, g, b)
    return hsl_to_rgb(h, min(1.0, s * amount), l)


def shift_lightness(r, g, b, target_l):
    h, s, l = rgb_to_hsl(r, g, b)
    return hsl_to_rgb(h, s, target_l)


def rgb_str(r, g, b):
    return f"{r},{g},{b}"


def generate_palette(colors):
    freq = Counter()
    for c in colors:
        freq[c] += 1
    sorted_colors = [c for c, _ in freq.most_common()]
    if not sorted_colors:
        sorted_colors = [(80, 120, 200)]

    primary = sorted_colors[0]
    accent = sorted_colors[min(2, len(sorted_colors)-1)]
    accent2 = sorted_colors[min(3, len(sorted_colors)-1)] if len(sorted_colors) > 3 else accent

    accent_bright = boost_sat(*accent, 1.5)
    accent2_bright = boost_sat(*accent2, 1.3)

    bg_darkest = shift_lightness(*primary, 0.06)
    bg_dark = shift_lightness(*primary, 0.10)
    bg_mid = shift_lightness(*primary, 0.14)
    bg_light = shift_lightness(*primary, 0.20)
    bg_lighter = shift_lightness(*primary, 0.26)

    text_bright = (230, 235, 245)
    text_normal = (200, 205, 215)
    text_dim = (145, 150, 160)
    text_muted = (105, 110, 120)

    h, s, l = rgb_to_hsl(*accent_bright)
    link = hsl_to_rgb(h, min(1.0, s), min(0.65, l + 0.1))
    h2, s2, l2 = rgb_to_hsl(*accent2_bright)
    visited = hsl_to_rgb(h2, min(0.8, s2), max(0.2, l2 - 0.1))

    sel_bg = accent_bright
    sel_fg = (255, 255, 255)

    return {
        "BackgroundAlternate": bg_light,
        "BackgroundNormal": bg_dark,
        "DecorationFocus": sel_bg,
        "DecorationHover": accent2_bright,
        "ForegroundActive": link,
        "ForegroundInactive": text_muted,
        "ForegroundLink": link,
        "ForegroundNegative": (220, 80, 80),
        "ForegroundNeutral": (180, 160, 100),
        "ForegroundNormal": text_normal,
        "ForegroundPositive": (100, 200, 120),
        "ForegroundVisited": visited,
        "SelectionBackground": sel_bg,
        "SelectionForeground": sel_fg,
        "ViewBackground": bg_mid,
        "ViewForeground": text_normal,
        "ViewHoverBackground": bg_light,
        "ViewHoverForeground": text_bright,
        "ViewAlternatingBackground": bg_lighter,
        "ViewFocusBackground": sel_bg,
        "WindowBackground": bg_darkest,
        "WindowForeground": text_normal,
        "ButtonBackground": bg_mid,
        "ButtonForeground": text_normal,
        "ButtonHoverBackground": bg_light,
        "ButtonHoverForeground": text_bright,
        "ButtonFocusBackground": sel_bg,
        "ButtonFocusForeground": sel_fg,
        "ButtonFlatBackground": bg_dark,
        "ButtonFlatForeground": text_dim,
        "HeaderBackground": bg_darkest,
        "HeaderForeground": text_normal,
        "HeaderHoverBackground": bg_light,
        "HeaderHoverForeground": text_bright,
        "HeaderFocusBackground": sel_bg,
        "HeaderFocusForeground": sel_fg,
        "FrameBackground": bg_dark,
        "FrameForeground": text_normal,
        "FrameHoverBackground": bg_light,
        "FrameHoverForeground": text_bright,
        "FrameFocusBackground": sel_bg,
        "FrameFocusForeground": sel_fg,
        "SliderBackground": bg_mid,
        "SliderForeground": sel_bg,
        "SliderHoverBackground": bg_light,
        "SliderHoverForeground": sel_bg,
        "SliderFocusBackground": sel_bg,
        "SliderFocusForeground": sel_fg,
        "TooltipBackground": bg_lighter,
        "TooltipForeground": text_bright,
        "Complementary.backgroundNormal": bg_dark,
        "Complementary.foregroundNormal": text_normal,
        "Complementary.backgroundAlternate": bg_light,
        "Complementary.decorationFocus": sel_bg,
        "Complementary.decorationHover": accent2_bright,
        "Complementary.foregroundActive": link,
        "Complementary.foregroundInactive": text_muted,
        "Complementary.foregroundLink": link,
        "Complementary.foregroundNegative": (220, 80, 80),
        "Complementary.foregroundNeutral": (180, 160, 100),
        "Complementary.foregroundPositive": (100, 200, 120),
        "Complementary.foregroundVisited": visited,
        "Complementary.selectionBackground": sel_bg,
        "Complementary.selectionForeground": sel_fg,
        "WM_activeBackground": sel_bg,
        "WM_activeBlend": sel_bg,
        "WM_activeForeground": sel_fg,
        "WM_inactiveBackground": bg_dark,
        "WM_inactiveBlend": bg_dark,
        "WM_inactiveForeground": text_dim,
        "WM_activeFrame": sel_bg,
        "WM_inactiveFrame": bg_dark,
    }


def write_colorscheme(palette, name):
    SCHEMES_DIR.mkdir(parents=True, exist_ok=True)
    path = SCHEMES_DIR / f"{name}.colors"
    h = hashlib.md5(str(time.time()).encode()).hexdigest()[:40]

    sections = [
        ("ColorEffects:Disabled", [
            ("ChangeSelectionColor", ""), ("Color", "23,23,23"),
            ("ColorAmount", "0"), ("ColorEffect", "0"),
            ("ContrastAmount", "0.65"), ("ContrastEffect", "1"),
            ("Enable", ""), ("IntensityAmount", "0.1"), ("IntensityEffect", "2"),
        ]),
        ("ColorEffects:Inactive", [
            ("ChangeSelectionColor", "true"), ("Color", "112,111,110"),
            ("ColorAmount", "0.025"), ("ColorEffect", "2"),
            ("ContrastAmount", "0.1"), ("ContrastEffect", "2"),
            ("Enable", "false"), ("IntensityAmount", "0"), ("IntensityEffect", "0"),
        ]),
        ("Colors:Button", [
            "BackgroundAlternate", "BackgroundNormal", "DecorationFocus", "DecorationHover",
            "ForegroundActive", "ForegroundInactive", "ForegroundLink", "ForegroundNegative",
            "ForegroundNeutral", "ForegroundNormal", "ForegroundPositive", "ForegroundVisited",
            "SelectionBackground", "SelectionForeground",
        ]),
        ("Colors:Selection", [
            "BackgroundAlternate", "BackgroundNormal", "DecorationFocus", "DecorationHover",
            "ForegroundActive", "ForegroundInactive", "ForegroundLink", "ForegroundNegative",
            "ForegroundNeutral", "ForegroundNormal", "ForegroundPositive", "ForegroundVisited",
        ]),
        ("Colors:Tooltip", [
            "BackgroundAlternate", "BackgroundNormal", "DecorationFocus", "DecorationHover",
            "ForegroundActive", "ForegroundInactive", "ForegroundLink", "ForegroundNegative",
            "ForegroundNeutral", "ForegroundNormal", "ForegroundPositive", "ForegroundVisited",
        ]),
        ("Colors:View", [
            "BackgroundAlternate", "BackgroundNormal", "DecorationFocus", "DecorationHover",
            "ForegroundActive", "ForegroundInactive", "ForegroundLink", "ForegroundNegative",
            "ForegroundNeutral", "ForegroundNormal", "ForegroundPositive", "ForegroundVisited",
            "SelectionBackground", "SelectionForeground", "AlternatingBackground", "FocusBackground",
        ]),
        ("Colors:Window", [
            "BackgroundAlternate", "BackgroundNormal", "DecorationFocus", "DecorationHover",
            "ForegroundActive", "ForegroundInactive", "ForegroundLink", "ForegroundNegative",
            "ForegroundNeutral", "ForegroundNormal", "ForegroundPositive", "ForegroundVisited",
        ]),
        ("Colors:Header", [
            "BackgroundAlternate", "BackgroundNormal", "DecorationFocus", "DecorationHover",
            "ForegroundActive", "ForegroundInactive", "ForegroundLink", "ForegroundNegative",
            "ForegroundNeutral", "ForegroundNormal", "ForegroundPositive", "ForegroundVisited",
            "SelectionBackground", "SelectionForeground",
        ]),
        ("Colors:Frame", [
            "BackgroundAlternate", "BackgroundNormal", "DecorationFocus", "DecorationHover",
            "ForegroundActive", "ForegroundInactive", "ForegroundLink", "ForegroundNegative",
            "ForegroundNeutral", "ForegroundNormal", "ForegroundPositive", "ForegroundVisited",
        ]),
        ("Colors:Complementary", [
            "BackgroundAlternate", "BackgroundNormal", "DecorationFocus", "DecorationHover",
            "ForegroundActive", "ForegroundInactive", "ForegroundLink", "ForegroundNegative",
            "ForegroundNeutral", "ForegroundNormal", "ForegroundPositive", "ForegroundVisited",
            "SelectionBackground", "SelectionForeground",
        ]),
    ]

    lines = []
    for section_name, keys in sections:
        lines.append(f"[{section_name}]")
        if isinstance(keys, list) and all(isinstance(k, tuple) for k in keys):
            for k, v in keys:
                lines.append(f"{k}={v}")
        elif section_name == "General":
            lines.append(f"ColorSchemeHash={h}")
            lines.append(f"Name={name}")
        else:
            for key in keys:
                if key in palette:
                    lines.append(f"{key}={rgb_str(*palette[key])}")
        lines.append("")

    lines.append("[General]")
    lines.append(f"ColorSchemeHash={h}")
    lines.append(f"Name={name}")
    lines.append("")

    lines.append("[WM]")
    wm_keys = [k for k in palette if k.startswith("WM_")]
    for wk in sorted(wm_keys):
        lines.append(f"{wk[3:]}={rgb_str(*palette[wk])}")

    path.write_text("\n".join(lines) + "\n")
    return path


def apply_scheme(name):
    try:
        r = subprocess.run(
            ["plasma-apply-colorscheme", name],
            capture_output=True, text=True, timeout=10
        )
        return r.returncode == 0
    except Exception:
        return False


def process_wallpaper(path):
    log(f"Processing: {path}")
    img = load_image(path)
    if not img:
        log("Failed to load image")
        return False
    colors = extract_colors(img)
    palette = generate_palette(colors)
    write_colorscheme(palette, SCHEME_NAME)
    ok = apply_scheme(SCHEME_NAME)
    if ok:
        log("Color scheme applied successfully")
    else:
        log("Failed to apply color scheme")
    return ok


def watch_with_inotify():
    """Use inotifywait to monitor the config file."""
    cmd = [
        "inotifywait", "-m", "-e", "modify,close_write",
        str(CONFIG_FILE)
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    return proc


def main():
    if not CONFIG_FILE.exists():
        log(f"ERROR: Config not found: {CONFIG_FILE}")
        sys.exit(1)

    wp = parse_wallpaper_path(CONFIG_FILE)
    if wp:
        log(f"Initial wallpaper: {wp}")
        process_wallpaper(wp)
    else:
        log("No wallpaper found")

    log("Starting inotifywait monitor...")
    inotify_proc = watch_with_inotify()
    last_wallpaper = wp

    try:
        for line in inotify_proc.stdout:
            line = line.strip()
            if not line:
                continue
            time.sleep(0.5)
            new_wp = parse_wallpaper_path(CONFIG_FILE)
            if new_wp and new_wp != last_wallpaper:
                last_wallpaper = new_wp
                process_wallpaper(new_wp)
            elif new_wp:
                log(f"Config changed but wallpaper same: {new_wp}")
    except KeyboardInterrupt:
        log("Interrupted")
    finally:
        inotify_proc.terminate()
        try:
            inotify_proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            inotify_proc.kill()


if __name__ == "__main__":
    main()
