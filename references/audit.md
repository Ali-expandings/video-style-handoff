# Completeness audit

Run this after drafting the handoff and before saving it. Fix every gap it finds, then fill in the Coverage report.

## 1. User messages

Go through the conversation from the first message to the last. For each user message, ask: did it contain a correction, preference, approval, rejection, or a fact about the video (a name, a deadline, a platform, a reference)?

- Corrections and preferences → **User preferences** and the section they belong to (e.g. "captions smaller" → Captions size, plus a preference line).
- Rejections and dropped attempts → **Rejected: do not do**, with the reason.
- Approvals ("perfect", "keep this") → mark the value as approved in its section. Approved values are the ones a future session must not change.
- Facts → the section they belong to.

Count them and write the number in the Coverage report ("14 corrections, 6 approvals, 4 rejections captured").

## 2. Hard-coded values

### With a shell
```bash
python3 <SKILL_DIR>/scripts/scan_values.py <project-dir> --check <handoff-file>
```
The scanner reports values found in the project that do not appear in the handoff: colors, fonts, easing curves, spring configs, durations and frame counts, dimensions and fps, audio levels, ffmpeg arguments, asset file references, package versions. For each one, either add it to the right section, or decide it's irrelevant (dead code, a library default nobody chose, an unused file). Re-run until only intentional omissions remain. Mention the count of intentional omissions in the Coverage report.

Useful flags:
- `--include-dir <dir>` to add a folder outside the project (shared assets, a brand kit).
- `--exclude <pattern>` to skip generated folders the default list misses.
- `--max-file-kb <n>` to scan larger files (default 512).

### Without a shell
Open each touched file and search for:
- `#` followed by 3, 4, 6 or 8 hex digits; `rgb(`, `rgba(`, `hsl(`, `oklch(`
- `font-family`, `fontFamily`, `loadFont`, `@font-face`, `.ttf`, `.otf`, `.woff`
- `cubic-bezier`, `Easing.`, `spring(`, `damping`, `stiffness`, `mass`, `ease-`
- `durationInFrames`, `fps`, `from=`, `delay`, `stagger`, `interpolate(`, `ms`, seconds values
- `width`, `height`, `1080`, `1920`, `scale`, `zoom`, `translate`
- `dB`, `LUFS`, `volume`, `loudnorm`, `silence`, `threshold`
- `ffmpeg`, `-crf`, `-preset`, `-b:v`, `-b:a`, `-pix_fmt`, `-vf`, `-af`
- file names ending in `.mp4 .mov .webm .png .jpg .svg .gif .mp3 .wav .m4a .srt .vtt .cube .glb .json`

Every hit must be in the handoff or deliberately left out.

## 3. Assets

List every file in the asset folders (`public/`, `assets/`, `media/`, `footage/`, `fonts/`, `audio/`, or whatever the project uses). Each one is in the Assets section with its purpose, or noted as unused.

## 4. Pipeline

Walk from raw material to the final file. Each step has an exact, copy-pasteable command and its inputs and outputs. If a step was done by hand in an app (a manual grade in DaVinci, a manual trim), write what was done and the settings.

## 5. New-editor test

Read the draft as someone who has never seen this project, holding only the handoff and the assets. Ask:

- What would they get wrong on the first try?
- What would they have to ask about?
- Which "obvious" choice would they make that the user already rejected?

Add whatever answers those questions.

## 6. Coverage report

Write at the top of the handoff:

```
## Coverage report
- Video type: <one line>
- Modules included: <list>
- Modules skipped: <module: reason>, ...
- New sections created: <list or none>
- User messages reviewed: <n>; corrections <n>, approvals <n>, rejections <n> captured
- Files scanned: <n> (scanner: yes/no; remaining unmatched values: <n>, all intentional)
- Could not verify: <values or "none">
- Environment: <e.g. Claude Code with shell / claude.ai without file access>
```
