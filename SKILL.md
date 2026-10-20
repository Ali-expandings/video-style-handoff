---
name: video-style-handoff
description: Capture the complete style of a video made with Claude (editing, motion graphics, captions, color, sound, pipeline, and the user's taste) into one handoff file, then load it later so the next video matches. Adapts to any video type: talking-head reels, promos without footage, explainers, product demos, screen recordings, podcast clips, interviews, ads, beat-synced edits, kinetic type, data viz, logo animations, 3D, AI-generated footage, vlogs. Works with any stack (Remotion, ffmpeg, HyperFrames, Three.js, HTML/CSS, Premiere/DaVinci/After Effects scripts). Use when the user says "save the style", "save my preferences", "handoff this video", "remember how we edited this", "make a style file", "wrap up the video", or, at the start of a session, "make it like last time", "use this handoff", "load my video style", or attaches a video style handoff file.
---

# Video Style Handoff

Turns everything that shaped a video into one markdown file that a person or a fresh model can rebuild the style from, and loads that file into the next session. It has two modes.

| The user wants | Mode |
|---|---|
| To save what was done in this session (end of a video, pausing work, "save the style") | **SAVE** |
| To make a new video like an earlier one, or continue one, from a handoff file | **LOAD** |

`<SKILL_DIR>` below means the folder that contains this file.

## Hard rules

1. **Exact values only.** Hex, px, frames, seconds, dB, LUFS, %, easing curves, spring configs, file paths, versions, commands. Take them from files and output, never from memory.
2. **Never invent.** A value that was never decided is written `not set`. A value that is visible in code but was never discussed is written with `(from code)`. Never fill a gap with a default.
3. **Files beat chat.** When the conversation and the files disagree, the files win, and the mismatch is noted in the handoff.
4. **The user's words are the most valuable evidence.** Every correction, approval and rejection the user gave goes into the file, quoted where possible.
5. **Adapt, don't fill a form.** Include only the modules this video actually has, and list the ones skipped with a reason. Create a new section for anything no module covers.
6. **No secrets.** Never write API keys, tokens or passwords into the handoff. Write where the secret lives instead ("env var `ELEVENLABS_API_KEY`").
7. **Do not skip the audit (Step 4).** It is the step that stops things from being missed.

## Environment check (first thing, both modes)

This skill runs in any Claude environment. Decide what you have:

- **Files and a shell** (Claude Code, Codex, Agent SDK, any CLI agent): read project files directly and run `python3 <SKILL_DIR>/scripts/scan_values.py` (standard library only, Python 3.8+).
- **Files but no shell**: read files with your file tools and do the scanner's job by hand, following `references/audit.md`.
- **No file access** (claude.ai chat, mobile): work from the conversation, any code shown in it, and attached files. Say in the Coverage report that project files could not be scanned. Deliver the handoff as a downloadable file or artifact if you can, otherwise as one markdown code block.

---

## SAVE mode

### Step 1: Gather the evidence

Read everything before writing anything:

- **The whole conversation**, every message. Mark each user correction ("no", "not like that", "smaller", "too fast"), approval ("perfect", "keep this") and rejection.
- **Every project file touched in the session**: composition/scene/timeline code, EDLs and cut lists, transcripts, subtitle files (.srt/.vtt/.ass), theme/brand/config files, CSS, props and JSON, shaders, ffmpeg and render scripts, `package.json` and lockfile versions, asset folders.
- **The output**: the rendered video, frames, screenshots or stills you can see.
- If a handoff for this project or brand already exists, read it. You will update it rather than create a second one.

If you have a shell, run the scanner on the project root now. It lists every hard-coded style value with file and line:

```bash
python3 <SKILL_DIR>/scripts/scan_values.py <project-dir> --out <project-dir>/.handoff-scan.md
```

### Step 2: Classify the video and pick the sections

Write the video type in one line. A mix is normal: "talking-head reel + motion graphics + B-roll + translated captions".

Open `references/modules.md`. It has:
- **Core sections**: always included, for every video.
- **Modules**: one per element a video can have (real footage, multi-cam, B-roll, captions, screen recording, voiceover, beat sync, kinetic type, data viz, logo animation, 3D/shaders, AI-generated media, brand, recurring graphic pieces, thumbnail, variants, accessibility). Check every module against the evidence. Include each one that applies. Record each skipped one with a one-line reason.
- **Anything else**: if the video has an element no module covers (a map animation, a game capture, a particle system, a split-screen reaction format), create a section for it, named clearly, with the same level of detail.

### Step 3: Write the handoff

Use `templates/handoff-template.md` as the skeleton. Fill it in order:

1. Coverage report (at the top; finish it after Step 4).
2. Core sections, then the included modules, then any new sections.
3. Decisions and why, Rejected (do not do), User preferences, Open issues, Next action, Restart prompt.

Style of writing: short lines and tables, no filler. Someone holding only this file and the assets must be able to rebuild the video. Write preferences as rules another model can follow ("Prefers X over Y", "Always Z", "Never W"), drawn from the user's corrections, not guesses about their taste.

### Step 4: Audit for completeness

Follow `references/audit.md`. In short:

1. **User messages.** Go through them one by one. Every correction, preference, approval and rejection must appear in the file. Count them.
2. **Hard-coded values.** Every color, number, duration, easing, size, threshold and path in the touched files must be in the handoff, or consciously left out as irrelevant. With a shell, run the check:
   ```bash
   python3 <SKILL_DIR>/scripts/scan_values.py <project-dir> --check <handoff-file>
   ```
   It lists values found in the code that do not appear in the handoff. Add each one or mark it irrelevant. Run it again until only intentional omissions remain.
3. **Assets.** Every file in the asset folders is listed with its purpose.
4. **Pipeline.** Each step from raw material to final file has its exact command.
5. **The new-editor test.** Ask: "If a new editor had only this file and the assets, what would they get wrong?" Add whatever answers that.

Then complete the Coverage report: video type, modules included and skipped, number of user corrections captured, files scanned, scanner result, values that could not be verified.

### Step 5: Save and report

- File name: `video-handoff_<project-slug>_<YYYY-MM-DD>.md`, saved in the project folder unless the user names another place. If the user keeps a notes system or docs folder (Obsidian vault, `docs/`, a wiki), offer to save a copy there too.
- If a handoff already exists for this project or brand, update it in place and add a "Changes since <date>" list at the top.
- Delete the temporary `.handoff-scan.md` if you created one.
- Tell the user, briefly: the file path, the video type and modules covered, and the 5 values you were least sure about so they can check them.

---

## LOAD mode

1. **Read the whole handoff first**, including the Coverage report and the "Rejected" list, before touching any new material.
2. **Treat it as rules.** Style sections, motion and edit rules, and the "do not do" list apply to this session. They are not suggestions.
3. **Check what still exists.** Verify every asset, component, preset, LUT, font and script path it lists. Report the missing ones. Check stack versions if the handoff pins them.
4. **Match the new video to the handoff.** If the new video is a different type (the handoff is a talking-head reel, the new one is a promo with no footage), say which sections carry over, which don't apply, and what is new and has no rule yet.
5. **Confirm back in five lines:** video type and format, visual rules (palette, fonts), motion and edit rules (timing, easing, cutting), captions and audio, top 3 things to avoid.
6. **Ask for the brief and material.** If the brief conflicts with the handoff, ask which wins before building.
7. **At the end of the new session,** run SAVE mode again. Update the same handoff if it's the same series or brand. Make a new one if the style changed on purpose.

## Files in this skill

- `references/modules.md`: core sections and every module, with the fields each one must capture.
- `references/audit.md`: the full completeness audit, including how to do it without a shell.
- `templates/handoff-template.md`: the output skeleton.
- `scripts/scan_values.py`: finds hard-coded style values in a project and checks a handoff against them.
- `examples/example-handoff.md`: a filled example for a talking-head reel with motion graphics.
