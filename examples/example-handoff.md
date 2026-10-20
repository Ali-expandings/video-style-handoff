# Video Style Handoff: Founder tips reel #3

<!-- Example only. The project, people and values are made up to show the level of detail expected. -->

## Coverage report
- Video type: talking-head reel + motion graphics + B-roll + Arabic/English captions
- Modules included: Real footage, B-roll and inserts, Captions, Brand profile, Recurring graphic pieces, Thumbnail
- Modules skipped: Multi-cam (one speaker, one camera) · Screen recording (none) · Voiceover (speaker's own voice) · Beat sync (music is background only) · Data viz, 3D, AI media, Logo animation (none in this video) · Variants (one 9:16 version only) · Accessibility (no specific checks done)
- New sections created: none
- User messages reviewed: 23; corrections 9, approvals 5, rejections 3 captured
- Files scanned: 31 (scanner: yes; 6 unmatched values left, all unused code in `src/old/`)
- Could not verify: music licence terms
- Environment: Claude Code with shell

## Snapshot
| Field | Value |
|---|---|
| Project | founder-tips-03 |
| Date | 2026-10-20 |
| Stack and versions | Remotion 4.0.526, ffmpeg 7.1, faster-whisper large-v3 |
| Project path | `~/videos/founder-tips` |
| Source material | `footage/IMG_4471.MOV` (2:41, iPhone 15 Pro, 4K 30 fps) |
| Output | `out/tips-03_final.mp4` |
| Purpose | 45 s tip reel: "stop pricing by the hour" |
| Audience / platform | early-stage founders · Instagram Reels, TikTok |

## Style in one paragraph
Direct and fast, with no dead air. A cut or visual change every 2 to 3 s. Big two-tone captions near the lower third. Graphics are flat, high contrast and appear with short, confident motion, never playful bounces. References: "explainer-channel pacing, but calmer", "keynote-style type".

## Format
| Ratio | Resolution | fps | Length | Safe zones | Adaptation |
|---|---|---|---|---|---|
| 9:16 | 1080×1920 | 30 | 0:45 | top 220 px, bottom 380 px, right 120 px kept clear | source was already vertical; scaled 4K → 1080 |

## Color
| Token | Hex | Used for |
|---|---|---|
| ink | #0e0e10 | card backgrounds, caption stroke |
| paper | #f5f3ee | card text, end card background |
| accent | #ffd400 | active caption word, numbers, underline |
| muted | #8a8a8f | secondary card text |

## Typography
| Role | Family | Source | Weight | Size | Line height | Tracking | Case | Effects |
|---|---|---|---|---|---|---|---|---|
| Captions (EN) | Inter | @remotion/google-fonts | 800 | 72 px | 1.05 | -0.5 px | as spoken | 6 px #0e0e10 stroke |
| Captions (AR) | Tajawal | @remotion/google-fonts | 800 | 76 px | 1.2 | 0 | n/a | 6 px #0e0e10 stroke, RTL |
| Hook card | Inter | @remotion/google-fonts | 900 | 120 px | 0.95 | -2 px | UPPER | none |
| Big number | Inter | @remotion/google-fonts | 900 | 260 px | 1 | -6 px | n/a | accent color |

## Layout and composition
Captions are centered horizontally with the baseline at y = 1340, so they never cover the mouth. Cards are 920 px wide with 48 px padding and 28 px radius, and have no shadow. Light grain everywhere at 4% opacity (from code).

## Motion and timing language
- Default easing: spring `{damping: 200, stiffness: 120, mass: 1}` (no overshoot). Exits use `Easing.in(Easing.cubic)`.
- Durations: enter 8 frames (0.27 s) · hold at least 45 frames · exit 6 frames · scene transition 0 (hard cut).
- Stagger: 3 frames between list items.
- Enter/exit styles: cards slide up 40 px and fade 0 → 1. Numbers count up over 18 frames.
- Idle motion: none.
- Banned motion: bounce, rotation, typewriter effect ("feels cheap").

## Real footage
- Cutting: silences below -35 dB and longer than 0.30 s removed, with 0.08 s padding kept before and after words (`scripts/cut.py --db -35 --min 0.30 --pad 0.08`). Retakes: the last take is kept. Filler words removed: "um", "uh", "so basically", "يعني".
- Pacing: average shot 2.4 s. A punch-in or insert at least every 3 s.
- Framing: face centered at x = 540, eyes at y ≈ 640. Punch-in alternates 100% ↔ 112% on every cut, over 0 frames (hard). Key-word emphasis: 112% → 120% over 10 frames.
- Look: `luts/warm-film.cube` at 60% strength, +5 contrast, -8 saturation. No denoise.

## B-roll and inserts
Full-screen inserts of 1.5 to 2.0 s, with hard cut in and out. Source: `broll/` (own phone clips). Rule: every number the speaker says gets either the Big number card or an insert.

## Captions
Two words per line max, one line. The active word turns accent #ffd400 and scales 1.0 → 1.06 over 3 frames. Timing comes from faster-whisper large-v3 word timestamps, with manual fixes at 0:12 and 0:31. Arabic version in `captions/ar.srt`, burned in for the AR export.

## Structure / timeline map
| Time | On screen | Copy / spoken line | Edit move | Motion move | Sound |
|---|---|---|---|---|---|
| 0:00–0:02 | Hook card over face | "STOP PRICING BY THE HOUR" | — | card slide-up | whoosh-01 |
| 0:02–0:11 | Face | "Here's why hourly pricing kills..." | 3 cuts, punch-ins | captions | — |
| 0:11–0:13 | Big number | "3×" | insert | count-up | pop-02 |
| ... | ... | ... | ... | ... | ... |
| 0:41–0:45 | End card | "Follow for tip #4" | — | fade-up | riser-01 |

## Audio
| Element | File / setting | Level | Notes |
|---|---|---|---|
| Voice | highpass 80 Hz, `afftdn=nr=12`, compressor 3:1 | — | — |
| Music | `audio/lofi-calm-92bpm.mp3` | -24 dB, ducks to -30 dB under voice | licence not verified |
| SFX | whoosh-01 on cards, pop-02 on numbers | -12 dB | nothing on captions |
| Master | `loudnorm=I=-14:TP=-1` | -14 LUFS, -1 dBTP | — |

## Brand profile
Handle @founder.tips at the bottom left of the end card only. CTA wording: "Follow for tip #<n>".

## Recurring graphic pieces
Hook card (0–2 s), Big number (on each number), End card (last 4 s). Components are listed in Reusable pieces.

## Thumbnail
Frame 0:03 with the hook text at 140 px, exported 1080×1920 to `out/cover.png`.

## Assets
| Path | Purpose | Source / licence |
|---|---|---|
| footage/IMG_4471.MOV | main talk | own |
| broll/*.mov (6 files) | inserts | own |
| luts/warm-film.cube | grade | own |
| audio/lofi-calm-92bpm.mp3 | music | not verified |
| sfx/whoosh-01.wav, sfx/pop-02.wav, sfx/riser-01.wav | SFX | own pack |

## Reusable pieces
| Name | File | Inputs | What it does |
|---|---|---|---|
| HookCard | src/kit/HookCard.tsx | text, durationInFrames | full-width hook over footage |
| BigNumber | src/kit/BigNumber.tsx | value, suffix | count-up number card |
| Captions | src/kit/Captions.tsx | words.json, lang | two-word, active-word captions |
| cut.py | scripts/cut.py | --db --min --pad | silence and retake cutter |

## Pipeline and render
1. Transcribe: `python scripts/transcribe.py footage/IMG_4471.MOV --model large-v3 --out words.json`
2. Cut: `python scripts/cut.py footage/IMG_4471.MOV --db -35 --min 0.30 --pad 0.08 --out cut.mp4`
3. Render: `npx remotion render Reel out/tips-03_raw.mp4`
4. Master: `ffmpeg -i out/tips-03_raw.mp4 -af loudnorm=I=-14:TP=-1 -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -b:a 192k out/tips-03_final.mp4`

Render time is about 3 min on an M2.

## Decisions and why
- Hard cuts only: transitions slowed the pace in the first draft.
- Two words per caption line: more than that was hard to read at phone size.

## Rejected: do not do
- Typewriter captions: "feels cheap".
- Emoji in captions: "not our brand".
- Zoom transitions between cuts: "too YouTube 2019".

## User preferences
- Prefers calm confidence over hype. No exclamation marks on screen.
- Always keeps a short pause before the punchline. Never cut it.
- Numbers always get a visual.

## Open issues
- Caption timing drifts about 2 frames late after 0:35. Re-check the word timestamps.

## Next action
Fix the caption drift after 0:35, then render the Arabic version.

## Restart prompt
```
Read the attached Video Style Handoff fully before doing anything. Treat its style sections and the "Rejected" list as rules. Check every asset and component path it lists and tell me which are missing. Confirm back in five lines: video type and format, palette and fonts, motion and edit rules, captions and audio, top 3 things to avoid. Then ask for the new brief and material. If the brief conflicts with the handoff, ask me which wins before building.
```
