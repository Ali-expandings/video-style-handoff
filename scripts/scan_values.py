#!/usr/bin/env python3
"""scan_values.py: find every hard-coded style value in a video project, and check a handoff against them.

Standard library only (Python 3.8+). Read-only: it never changes project files.

  python3 scan_values.py <project-dir>                       list values found, grouped by category
  python3 scan_values.py <project-dir> --out scan.md         write the list to a file
  python3 scan_values.py <project-dir> --check handoff.md    list values NOT found in the handoff

Categories: colors, fonts, easing and springs, timing, dimensions and transforms, audio levels,
ffmpeg arguments, asset references, asset files on disk, stack versions, interpolate ranges.

The check is deliberately strict: a key=value pair only counts as covered when the value and a word
from its key appear on the same line of the handoff. A value reported as missing may still be fine
to leave out (dead code, an untouched library default); decide each one.
"""
import argparse
import json
import os
import re
import sys
from collections import OrderedDict
from pathlib import Path

SKIP_DIRS = {
    "node_modules", ".git", "out", "dist", "build", ".next", ".cache", "__pycache__", ".venv", "venv",
    "coverage", ".turbo", ".remotion", ".vercel", ".netlify", "target", ".idea", ".vscode", "renders",
}
TEXT_EXT = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".json", ".css", ".scss", ".sass", ".less", ".html",
    ".htm", ".vue", ".svelte", ".py", ".sh", ".bash", ".zsh", ".yaml", ".yml", ".toml", ".srt", ".vtt",
    ".ass", ".glsl", ".frag", ".vert", ".wgsl", ".jsxbin", ".lua", ".txt", ".cfg", ".ini", ".env.example",
}
SKIP_FILES = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb", "tsconfig.json", ".eslintrc.json"}
MEDIA_EXT = {
    ".mp4", ".mov", ".webm", ".mkv", ".avi", ".m4v", ".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif",
    ".avif", ".heic", ".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg", ".srt", ".vtt", ".ass", ".cube",
    ".3dl", ".glb", ".gltf", ".fbx", ".obj", ".ttf", ".otf", ".woff", ".woff2", ".lottie", ".riv",
}
VIDEO_PKG = re.compile(
    r"remotion|three|@react-three|hyperframes|gsap|framer-motion|motion|lottie|ffmpeg|fluent-ffmpeg|"
    r"whisper|elevenlabs|mediabunny|pixi|p5|theatre|rive|@ffmpeg|canvas|sharp|puppeteer|playwright"
)

HEX = re.compile(r"(?<![\w&])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})\b")
COLOR_FN = re.compile(r"\b(?:rgba?|hsla?|oklch|oklab|lab|lch)\([^)]{3,80}\)")
FONT_FAMILY = re.compile(r"""(fontFamily|font-family)\s*[:=]\s*(?:['"`]([^'"`\n]{2,80})['"`]|([^;'"`\n{}]{2,80}))""")
FONT_LOAD = re.compile(r"""@remotion/google-fonts/([\w-]+)|loadFont\(\s*['"`]([^'"`]+)""")
FONT_FACE_SRC = re.compile(r"""[\w./-]+\.(?:ttf|otf|woff2?)\b""")
BEZIER = re.compile(r"(?:cubic-bezier|Easing\.bezier)\(\s*[-\d.\s,]+\)")
EASING_FN = re.compile(r"\bEasing\.(?!bezier)\w+(?:\((?:[^()]|\([^()]*\))*\))?")
CSS_EASE = re.compile(r"\b(?:ease-in-out|ease-in|ease-out|steps\(\d+[^)]*\))\b")
SPRING_KEY = re.compile(r"\b(damping|stiffness|mass|overshootClamping|tension|friction|bounce|velocity)\s*[:=]\s*([\w.-]+)")
TIMING_KEY = re.compile(
    r"\b(durationInFrames|fps|delay|stagger|staggerFrames|from|startFrom|endAt|trimBefore|trimAfter|"
    r"premountFor|duration|durationMs|transitionDuration|holdFrames|enterFrames|exitFrames|playbackRate|"
    r"framesPerWord|wordsPerLine|maxLines|silenceThreshold|minSilence|padding(?:Before|After)Ms?)"
    r"\s*[:=]\s*\{?\s*(-?[\d.]+(?:ms|s)?)\b"
)
CSS_TIME = re.compile(r"\b(?:transition|animation)(?:-duration|-delay)?\s*:\s*([^;\n]{2,80})")
DIM_KEY = re.compile(
    r"\b(width|height|fontSize|font-size|letterSpacing|letter-spacing|lineHeight|line-height|borderRadius|"
    r"border-radius|padding|margin|gap|top|left|right|bottom|scale|zoom|blur|opacity|strokeWidth|"
    r"stroke-width|WebkitTextStroke|-webkit-text-stroke|textShadow|text-shadow|boxShadow|box-shadow|fontWeight|font-weight|"
    r"""translateX|translateY|rotate|maxWidth|max-width)\s*[:=]\s*\{?\s*['"`]?(-?[\d.]+(?:px|%|em|rem|vh|vw|deg)?"""
    r"(?:\s+-?[\d.]+(?:px|%|em|rem)?){0,3}(?:\s+(?:rgba?\([^)]*\)|#[0-9a-fA-F]{3,8}))?)"
)
AUDIO_LEVEL = re.compile(r"-?\d+(?:\.\d+)?\s*(?:dBTP|dBFS|LUFS|LU|dB)\b")
AUDIO_KEY = re.compile(r"\b(volume|gain|ducking|duckTo|musicVolume|voiceVolume|sfxVolume)\s*[:=]\s*\{?\s*(-?\d[\d.]*)")
AUDIO_FILTER = re.compile(r"\b(?:loudnorm|silencedetect|silenceremove|afftdn|highpass|lowpass|acompressor|equalizer|volume|sidechaincompress|dynaudnorm)=[\w.:-][^\s'\"`,\]}]*")
FFMPEG_ARG = re.compile(r"""(?:['"`]|\s)-(crf|preset|b:v|b:a|maxrate|bufsize|pix_fmt|r|c:v|c:a|vcodec|acodec|profile:v|tune|ar|ac|movflags|lut3d)(?:['"`]\s*,\s*['"`]|\s+)([^\s'"`,\]]+)""")
LUT_FILTER = re.compile(r"\blut3d=[^\s'\"`,\]]+")
ASSET_REF = re.compile(r"""[\w./@-]+\.(?:mp4|mov|webm|mkv|m4v|png|jpe?g|webp|svg|gif|avif|mp3|wav|m4a|aac|flac|ogg|srt|vtt|ass|cube|3dl|glb|gltf|fbx|ttf|otf|woff2?|lottie|riv)\b""", re.I)
INTERP = re.compile(r"interpolate\(\s*[\w.]+\s*,\s*\[([^\]]{1,60})\]\s*,\s*\[([^\]]{1,80})\]")

SYNONYMS = {
    "width": ["resolution", "size", "×", "x"], "height": ["resolution", "size", "×", "x"],
    "fps": ["frame rate", "framerate"], "durationinframes": ["frames", "length", "duration"],
    "from": ["start", "at", "frame"], "crf": ["quality"], "pix_fmt": ["pixel"],
}


def camel_words(key):
    parts = re.sub(r"([a-z])([A-Z])", r"\1 \2", key).replace("-", " ").replace("_", " ").replace(":", " ").split()
    words = [p.lower() for p in parts if len(p) >= 2]
    words += SYNONYMS.get(key.lower().replace("-", ""), [])
    words.append(key.lower())
    return list(dict.fromkeys(words))


class Findings:
    def __init__(self):
        self.data = OrderedDict()  # category -> value -> {"key":..., "val":..., "locs": [...]}

    def add(self, cat, value, loc, key=None, val=None):
        value = value.strip()
        if not value:
            return
        bucket = self.data.setdefault(cat, OrderedDict())
        item = bucket.setdefault(value, {"key": key, "val": val, "locs": []})
        if len(item["locs"]) < 50:
            item["locs"].append(loc)


def iter_files(roots, include_md, max_bytes, extra_excludes, exclude_names):
    for root in roots:
        root = Path(root)
        if root.is_file():
            yield root, root.parent
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not any(x in d for x in extra_excludes)]
            for name in filenames:
                p = Path(dirpath) / name
                if name in SKIP_FILES or name in exclude_names or any(x in str(p) for x in extra_excludes):
                    continue
                yield p, root


def scan(roots, include_md=False, max_kb=512, extra_excludes=(), exclude_names=()):
    f = Findings()
    max_bytes = max_kb * 1024
    files_scanned = 0
    for path, root in iter_files(roots, include_md, max_bytes, extra_excludes, set(exclude_names)):
        try:
            rel = str(path.relative_to(root))
        except ValueError:
            rel = str(path)
        ext = path.suffix.lower()
        if ext in MEDIA_EXT:
            try:
                size = path.stat().st_size
            except OSError:
                size = 0
            f.add("Asset files on disk", rel, f"{size / 1024 / 1024:.1f} MB" if size > 1024 * 1024 else f"{size // 1024} KB")
            if ext not in {".srt", ".vtt", ".ass", ".svg"}:
                continue
        is_md = ext in {".md", ".mdx"}
        if not (ext in TEXT_EXT or (is_md and include_md) or ext in {".srt", ".vtt", ".ass", ".svg"}):
            continue
        try:
            if path.stat().st_size > max_bytes:
                f.add("Skipped (too large)", rel, f"> {max_kb} KB")
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        files_scanned += 1
        if path.name == "package.json":
            scan_package(text, rel, f)
            continue
        if ext in {".srt", ".vtt", ".ass"}:
            f.add("Subtitle files", rel, f"{text.count('-->') or text.count('Dialogue:')} cues")
            continue
        for n, line in enumerate(text.splitlines(), 1):
            if len(line) > 2000:
                line = line[:2000]
            loc = f"{rel}:{n}"
            for m in HEX.finditer(line):
                f.add("Colors", m.group(0).lower(), loc)
            for m in COLOR_FN.finditer(line):
                f.add("Colors", re.sub(r"\s+", " ", m.group(0)), loc)
            for m in FONT_FAMILY.finditer(line):
                if m.group(2):
                    fam = m.group(2).strip()
                else:
                    fam = m.group(3).strip()
                    if m.group(1) == "fontFamily":
                        fam = ""  # unquoted in JS = a variable; its quoted definition is caught where it's set
                    elif fam.startswith(("var(", "inherit", "$", "{")):
                        fam = ""
                if fam:
                    f.add("Fonts", fam, loc)
            for m in FONT_LOAD.finditer(line):
                f.add("Fonts", m.group(1) or m.group(2), loc)
            for m in BEZIER.finditer(line):
                f.add("Easing and springs", re.sub(r"\s+", "", m.group(0)), loc)
            for m in EASING_FN.finditer(line):
                f.add("Easing and springs", re.sub(r"\s+", "", m.group(0)), loc)
            for m in CSS_EASE.finditer(line):
                f.add("Easing and springs", m.group(0), loc)
            for m in SPRING_KEY.finditer(line):
                f.add("Easing and springs", f"{m.group(1)}: {m.group(2)}", loc, m.group(1), m.group(2))
            for m in TIMING_KEY.finditer(line):
                f.add("Timing", f"{m.group(1)}: {m.group(2)}", loc, m.group(1), m.group(2))
            for m in CSS_TIME.finditer(line):
                f.add("Timing", m.group(0).strip(), loc)
            for m in INTERP.finditer(line):
                f.add("Interpolate ranges", f"[{m.group(1).strip()}] -> [{m.group(2).strip()}]", loc)
            for m in DIM_KEY.finditer(line):
                f.add("Dimensions and transforms", f"{m.group(1)}: {m.group(2).strip()}", loc, m.group(1), m.group(2).strip())
            for m in AUDIO_LEVEL.finditer(line):
                f.add("Audio levels and filters", re.sub(r"\s+", " ", m.group(0)), loc)
            for m in AUDIO_KEY.finditer(line):
                f.add("Audio levels and filters", f"{m.group(1)}: {m.group(2)}", loc, m.group(1), m.group(2))
            for m in AUDIO_FILTER.finditer(line):
                f.add("Audio levels and filters", m.group(0), loc)
            for m in FFMPEG_ARG.finditer(line):
                f.add("Encode / ffmpeg arguments", f"-{m.group(1)} {m.group(2)}", loc, m.group(1), m.group(2))
            for m in LUT_FILTER.finditer(line):
                f.add("Encode / ffmpeg arguments", m.group(0), loc)
            for m in ASSET_REF.finditer(line):
                ref = m.group(0)
                if not ref.startswith(("http", "//")):
                    f.add("Asset references in code", ref, loc)
            for m in FONT_FACE_SRC.finditer(line):
                f.add("Fonts", Path(m.group(0)).name, loc)
    return f, files_scanned


def scan_package(text, rel, f):
    try:
        pkg = json.loads(text)
    except ValueError:
        return
    for section in ("dependencies", "devDependencies"):
        for name, ver in (pkg.get(section) or {}).items():
            cat = "Stack versions (video-related)" if VIDEO_PKG.search(name) else "Stack versions (other)"
            f.add(cat, f"{name}@{ver}", rel, name, str(ver).lstrip("^~="))
    for name, cmd in (pkg.get("scripts") or {}).items():
        if re.search(r"remotion|render|ffmpeg|export|build|studio|preview|transcribe", f"{name} {cmd}"):
            f.add("Render / build scripts", f"{name}: {cmd}", rel)


def norm(s):
    return re.sub(r"\s+", "", s.lower())


def covered(cat, value, item, handoff, handoff_lines, handoff_norm):
    if cat in {"Interpolate ranges", "Stack versions (other)", "Skipped (too large)"}:
        return True  # reviewed by hand, not auto-checked
    if cat == "Colors":
        v = value.lower()
        if v in handoff.lower():
            return True
        if re.fullmatch(r"#[0-9a-f]{3}", v):
            return ("#" + "".join(c * 2 for c in v[1:])) in handoff.lower()
        return norm(v) in handoff_norm
    if cat in {"Asset files on disk", "Asset references in code", "Subtitle files"}:
        return Path(value).name.lower() in handoff.lower()
    if cat == "Stack versions (video-related)":
        name, ver = item["key"], item["val"]
        return any(name.lower() in l and ver in l for l in handoff_lines)
    if cat == "Render / build scripts":
        cmd = value.split(":", 1)[1].strip()
        return norm(cmd) in handoff_norm
    if item.get("key") is not None:
        val = item["val"].lower().strip()
        words = camel_words(item["key"])
        nums = re.findall(r"-?[\d.]+", val) or [val]
        for l in handoff_lines:
            if all(re.search(rf"(?<![\d.]){re.escape(n)}(?![\d])", l) for n in nums) and any(w in l for w in words):
                return True
        return False
    return norm(value) in handoff_norm


def render(f, files_scanned, roots, check=None):
    out = []
    title = "Values not found in the handoff" if check else "Style values found in the project"
    out.append(f"# {title}\n")
    out.append(f"Scanned: {', '.join(str(r) for r in roots)} · {files_scanned} text files\n")
    if check:
        out.append(f"Checked against: {check}\n")
        out.append("Each item below was found in the project but not in the handoff. Add it to the right section, "
                   "or decide it's irrelevant (dead code, untouched default, unused file). Interpolate ranges and "
                   "non-video packages are not auto-checked; review them by hand.\n")
        handoff = Path(check).read_text(encoding="utf-8", errors="ignore")
        handoff_lines = [l.lower() for l in handoff.splitlines()]
        handoff_norm = norm(handoff)
    total = 0
    summary = []
    body = []
    for cat, bucket in f.data.items():
        items = []
        for value, item in bucket.items():
            if check and covered(cat, value, item, handoff, handoff_lines, handoff_norm):
                continue
            locs = item["locs"]
            shown = ", ".join(locs[:3]) + (f" (+{len(locs) - 3} more)" if len(locs) > 3 else "")
            items.append(f"- `{value}` — {shown}")
        if check and cat in {"Interpolate ranges", "Stack versions (other)"}:
            items = []
            if bucket:
                summary.append(f"- {cat}: {len(bucket)} to review by hand")
            continue
        if not items:
            continue
        total += len(items)
        summary.append(f"- {cat}: {len(items)}")
        body.append(f"\n## {cat} ({len(items)})\n")
        body.extend(items)
    out.append("## Summary\n")
    out.extend(summary or ["- nothing found"])
    out.append(f"\nTotal: {total}\n")
    out.extend(body)
    return "\n".join(out) + "\n", total


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", nargs="+", help="project folder(s) or file(s) to scan")
    ap.add_argument("--check", metavar="HANDOFF", help="handoff file to check coverage against")
    ap.add_argument("--out", metavar="FILE", help="write the report to a file instead of stdout")
    ap.add_argument("--include-dir", action="append", default=[], help="extra folder to scan (repeatable)")
    ap.add_argument("--exclude", action="append", default=[], help="skip paths containing this text (repeatable)")
    ap.add_argument("--include-md", action="store_true", help="also scan .md/.mdx files")
    ap.add_argument("--max-file-kb", type=int, default=512, help="skip text files larger than this (default 512)")
    a = ap.parse_args()

    roots = [Path(p).expanduser().resolve() for p in a.project + a.include_dir]
    for r in roots:
        if not r.exists():
            sys.exit(f"not found: {r}")
    exclude_names = {".handoff-scan.md"}
    if a.check:
        exclude_names.add(Path(a.check).name)
    if a.out:
        exclude_names.add(Path(a.out).name)
    f, n = scan(roots, a.include_md, a.max_file_kb, a.exclude, exclude_names)
    report, total = render(f, n, roots, a.check)
    if a.out:
        Path(a.out).write_text(report, encoding="utf-8")
        print(f"wrote {a.out} ({total} items)")
    else:
        sys.stdout.write(report)


if __name__ == "__main__":
    main()
