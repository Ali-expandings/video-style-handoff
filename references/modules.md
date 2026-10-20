# Sections and modules

Core sections go into every handoff. Modules go in only when the video has that element. Each list below is the minimum to capture. Add anything else the evidence shows.

Mark values: exact value · `(from code)` if never discussed · `not set` if never decided.

---

## Core sections (always)

### Snapshot
Project name · date · video type (one line) · stack and versions (e.g. Remotion 4.0.x, ffmpeg 7, Node 22) · project path or repo · source material path(s) · final output path(s) · one-line purpose · audience · platform(s).

### Style in one paragraph
The feel in plain words ("fast, punchy, bold captions, clean motion, never cheesy"). 3 to 5 reference words, creators, brands or videos the user pointed at.

### Format
Aspect ratio · resolution · fps · total length · platform safe zones and where the platform UI covers the frame · background color behind content · how mismatched source was adapted (crop, blur fill, letterbox, split).

### Color
Every color as a token: name · hex (and alpha) · where it's used. Gradients: stops, angle, type. Dark/light rules. Color for states (highlight, active word, warning).

### Typography
Per font: family · source (Google Fonts, local file path, system) · weights used · size per role (hook, headline, body, caption, number, lower third, CTA) · line height · letter spacing · case · alignment · text direction (RTL/LTR) and mixed-script handling · effects (stroke width and color, shadow, highlight box, glow, gradient fill).

### Layout and composition
Grid and margins · padding · placement rules (where text sits relative to the subject's face, the safe zones, the center) · recurring containers or cards · corner radius · borders · shadows · textures, grain, noise, vignette · z-order rules (what's always on top).

### Motion and timing language
The most important visual section. Be exact.
- Default easing: curve values (`cubic-bezier(...)`, `Easing.bezier(...)`) or spring config (damping, stiffness, mass, overshootClamping).
- Durations in frames and seconds: enter, hold, exit, transition.
- Stagger between items.
- Enter/exit styles: fade, slide (distance in px), scale (from/to), mask, blur, pop.
- Scene transitions: type and length in frames.
- Idle motion: float, pulse, drift (amplitude, period).
- Camera moves inside graphics: zoom, pan, parallax amounts.
- Banned motion ("no bounce", "no rotation over 5°").

### Structure / timeline map
Table: time range · what's on screen (footage / insert / graphic) · copy or spoken line · edit move · motion move · sound. Plus the reusable pattern if one exists (hook → problem → proof → CTA).

### Copy and voice
Tone of on-screen text · max words per screen · language(s) · punctuation and number style · emoji use · the actual lines used.

### Audio
Music: file, source, licence, BPM, mood, volume in dB, where it ducks and by how much. SFX: each file and what triggers it. Voice: cleanup chain (denoise, EQ, compressor settings). Mix: loudness target (e.g. −14 LUFS integrated, −1 dBTP), fades. Whether motion is synced to beats.

### Assets
Every file used: footage, logos, images, icons, fonts, LUTs, music, SFX, 3D models, data files. Path · what it's for · source or licence where known.

### Reusable pieces
Components, presets, templates, scripts and helper functions built in the session: name · file · inputs/props · what it does. These let the next video reuse instead of rebuild.

### Pipeline and render
Every step from raw material to final file, in run order, with the exact command for each (e.g. transcribe → cut → reframe → grade → graphics → captions → mix → render → compress). Codec, bitrate/CRF, pixel format, audio codec and bitrate, container. Output path. Render time.

### Decisions and why
One line per decision: what was chosen and the reason.

### Rejected: do not do
Everything the user said no to, or that was tried and dropped. The reason. The user's words in quotes where possible.

### User preferences
The user's taste written as rules another model can follow. Drawn from corrections and approvals, never guessed.

### Open issues
Unfinished work, known bugs ("the video jumps back at 0:42"), ideas the user wanted to try next.

### Next action
The ONE thing to do first in the next session.

### Restart prompt
A short, ready-to-paste prompt for a fresh session: read this handoff, load the style, confirm the key values in five lines, then ask for the new brief and material.

---

## Modules (only when the video has the element)

### Real footage
- Clips: file · length · camera/device · resolution/fps · who or what is on screen · quality issues (noise, shake, bad light, bad audio).
- Cutting rules: silence threshold (dB) · minimum pause length cut · padding kept before/after words · how retakes are detected and which take is kept · filler words removed (list them, in every language used) · what is always kept (breaths, laughs, pauses for emphasis) · average shot length · max time without a visual change · jump-cut handling (punch-in, cover with B-roll, left raw).
- Final cut list or EDL with timestamps, or its path.
- Framing / virtual camera: face tracking tool and settings · where the face sits in frame · headroom · punch-in amounts (e.g. 100% → 115%) and their triggers (each cut, key words, emphasis) · zoom easing and duration · handheld/shake effect amount · reframing from horizontal to vertical.
- Look: grade, LUT file and strength, exposure/contrast/saturation/temperature changes, skin tone notes.
- Cleanup: denoise, stabilization, sharpening, background cutout or blur (tool, model, settings).

### Multi-person / multi-cam
Speaker-switching rules (who is shown when) · split layouts and their proportions · angle choice rules · audio source per speaker · sync method.

### B-roll and inserts
Kinds of inserts (stock, screen captures, memes, code, images) · sources and licences · duration of each · full-screen vs picture-in-picture (size, position, border) · entry and exit animation · rules for when to insert ("every number gets a visual", "no insert longer than 2 s").

### Captions / subtitles
Font · size · position and how it avoids the face and platform UI · text and box colors · active-word highlight style · words per line · max lines · per-word animation · emoji and keyword emphasis rules · casing · transcription tool and model · timing corrections made · translations and .srt/.vtt paths · burned-in or sidecar.

### Screen recording / product demo / UI
Capture tool and resolution · cursor style and size · click effects · zoom-to-region moves (scale, duration, easing) · device frames · window chrome shown or hidden · mock or real data used · privacy blurs.

### Voiceover / narration
Script file · provider and voice ID or name · speed and style settings · takes kept · how visuals are timed to narration (timeline file, word timestamps).

### Music-driven / beat-synced
Track · BPM · beat map or marker file · which visual events land on which beats · how sync was computed.

### Kinetic typography
Text reveal system (per letter, word, line) · per-unit timing · emphasis rules (which words get size, color or motion) · line breaking rules.

### Data viz / charts
Data source and file · chart types · number formatting (decimals, units, separators, currency) · count-up timing and easing · axis and gridline style · highlight rules.

### Logo / brand animation
Logo files and versions · build-up sequence step by step with timing · end state · sound sting · where and how long the logo appears in other videos.

### 3D / WebGL / shaders
Scene setup · camera (type, FOV, path) · lights · materials · models and paths · shader uniforms and their values · postprocessing passes and settings · performance settings used for rendering.

### AI-generated media
Tool and model for each piece · prompts (full text) · seeds · settings (resolution, steps, guidance, duration) · which generations were kept and why · upscaling or cleanup applied · licence/usage notes.

### Brand profile
Brand name · logo placement and size rules · handles · CTA wording · tone words · path to a saved brand profile if one exists.

### Recurring graphic pieces
For each one used (hook card, quote card, big number, list, lower third, CTA, end card, progress bar, chapter title): what it looks like · how it moves · how long it stays · which component builds it.

### Thumbnail / cover
Layout · text · frame or image chosen · fonts and colors if different from the video · export size.

### Variants
Other ratios, languages, cut-downs, A/B versions: how each differs and its output path.

### Accessibility
Contrast checks · caption readability · flashing limits · reduced-motion version if any.

### Anything else
If the video has an element not listed here, add a section for it with the same depth: what it is, every value that shapes it, the files that build it, and the user's feedback on it.
