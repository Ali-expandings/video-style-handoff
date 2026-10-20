# video-style-handoff

A skill for Claude that saves the complete style of a video into one handoff file, and loads that file into a later session so the next video matches.

You spend a session getting a video right: the cuts, the captions, the colors, the easing, the music levels, and a dozen "no, smaller" corrections. Then the session ends and all of it is gone. This skill writes it down: every value, every rejected idea, and your taste as rules. A fresh session, or another person, can pick it up from there.

## What it captures

It adapts to the video. There's no fixed form. Claude works out the video type and includes what applies:

- **Always:** format, colors, fonts, layout, motion and timing (easing curves, spring configs, durations in frames), a timeline map, copy, audio, assets, reusable components, the render pipeline with exact commands, decisions, a "do not do" list, your preferences, open issues, and the next action.
- **When the video has it:** footage cutting rules (silence threshold, padding, retakes, filler words), virtual camera and punch-ins, color grade and LUTs, B-roll, captions, multi-cam, screen recordings, voiceover, beat sync, kinetic type, data viz, logo animation, 3D and shaders, AI-generated media, brand profile, thumbnails, variants, accessibility.
- **Anything else:** if the video has an element no module covers, Claude creates a section for it.

Before saving, Claude audits the draft. It checks every one of your messages for corrections, scans the project for hard-coded values that the handoff missed, checks every asset, and checks every pipeline step. The result goes at the top of the file as a coverage report.

Works with any stack: Remotion, ffmpeg, HyperFrames, Three.js, HTML/CSS, Premiere / DaVinci / After Effects scripts, CapCut-style pipelines.

## Install

### Easiest: paste this prompt into your agent

Works in Claude Code, Codex, or any agent with a shell. Copy it, paste it into a new session, and the agent installs the skill for you.

```
Install the "video-style-handoff" skill from https://github.com/Ali-expandings/video-style-handoff for me.

1. Work out which tool you are running in and pick the skills folder:
   - Claude Code: ~/.claude/skills/video-style-handoff (or <project>/.claude/skills/video-style-handoff if I say "this project only")
   - Codex: ~/.codex/skills/video-style-handoff
   - Another agent: its personal skills folder; if you don't know it, ask me.
2. If that folder already exists, run `git -C <folder> pull` to update it instead of cloning again.
3. Otherwise run: git clone https://github.com/Ali-expandings/video-style-handoff.git <folder>
   If git is not available, download https://github.com/Ali-expandings/video-style-handoff/releases/latest/download/video-style-handoff.zip and unzip it so that <folder>/SKILL.md exists.
4. Check that <folder>/SKILL.md exists and read it so you know what the skill does.
5. If python3 is installed, run `python3 <folder>/scripts/scan_values.py --help` to confirm the scanner works. It is optional; the skill still works without Python.
6. Don't install anything else and don't change any other settings.
7. Tell me in two lines: where it was installed, and whether I need to start a new session for it to show up. Then show me how to use it: "save the style of this video as a handoff" at the end of a video, and "use this handoff" at the start of the next one.
```

On **claude.ai** (no shell), the agent can't install skills itself. Download `video-style-handoff.zip` from the [latest release](https://github.com/Ali-expandings/video-style-handoff/releases/latest) and upload it under Settings → Capabilities → Skills.

### Manual install

**Claude Code** (personal skills folder):
```bash
git clone https://github.com/Ali-expandings/video-style-handoff.git ~/.claude/skills/video-style-handoff
```
For one project only, clone it into `<project>/.claude/skills/video-style-handoff` instead.

**Any agent that supports the skills CLI** (Claude Code, Codex, Cursor and others):
```bash
npx skills add Ali-expandings/video-style-handoff
```

**claude.ai** (web, desktop, mobile): download `video-style-handoff.zip` from the [latest release](https://github.com/Ali-expandings/video-style-handoff/releases/latest), then upload it under Settings → Capabilities → Skills.

**Codex**:
```bash
git clone https://github.com/Ali-expandings/video-style-handoff.git ~/.codex/skills/video-style-handoff
```

Requirements: none to use the skill. The optional scanner needs Python 3.8 or newer and uses only the standard library.

## Use

At the end of a video session:
> save the style of this video as a handoff

At the start of the next one, with the file attached or its path given:
> use this handoff, make the next video like this one

Other phrases that trigger it: "save my preferences", "handoff this video", "remember how we edited this", "make it like last time", "load my video style".

The handoff is saved as `video-handoff_<project>_<date>.md` in your project folder. If you work on the same series or brand again, the file is updated in place rather than copied. See [examples/example-handoff.md](examples/example-handoff.md) for a filled example.

## The scanner

`scripts/scan_values.py` finds every hard-coded style value in a project (colors, fonts, easing, springs, durations, dimensions, audio levels, ffmpeg arguments, asset references, package versions) and checks which ones a handoff is missing.

```bash
python3 scripts/scan_values.py ~/videos/my-reel                       # list what's in the project
python3 scripts/scan_values.py ~/videos/my-reel --check handoff.md    # list what the handoff missed
```

It is read-only and never changes your files. The skill runs it for you when a shell is available. Without a shell, as on claude.ai, Claude does the same audit by hand and says so in the coverage report.

## Files

```
SKILL.md                      the skill: SAVE and LOAD modes
references/modules.md         core sections and every module, with fields to capture
references/audit.md           the completeness audit
templates/handoff-template.md output skeleton
scripts/scan_values.py        value scanner and coverage checker
examples/example-handoff.md   a filled example
```

## License

MIT
